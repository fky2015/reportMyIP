from flask import Flask, request
import json
import dbio
import time
import os
import requests

app = Flask(__name__)

config = {}
if os.path.exists('config.json'):
    try:
        with open('config.json') as f:
            config = json.load(f)
    finally:
        pass


def wrap_list(ls: list)->dict:
    return [dict(zip(['hostname', 'uid', 'ip_address', 'status',
                      'update_time', 'info'], i[1:]))
            for i in ls]


@app.route('/hello')
def hello_world():
    return "Hello World!"


@app.route('/hosts')
def hosts():
    res = dbio.getAll()
    res = wrap_list(res)
    return json.dumps(res)


@app.route('/host/<hostname>', methods=['DELETE'])
def del_host(hostname):
    try:
        dbio.delete(hostname)
    except Exception as e:
        print(e)
        return json.dumps({"status": "fail"})
    return json.dumps({"status": "success"})


@app.route('/hosts', methods=['DELETE'])
def del_hosts():
    try:
        dbio.delAll()
    except Exception as e:
        print(e)
        return json.dumps({"status": "fail"})
    return json.dumps({"status": "success"})


@app.route('/host/<hostname>')
def host(hostname):
    return json.dumps(wrap_list(dbio.get(hostname)))


@app.route('/host', methods=['POST'])
def update_host():
    print(str(request.args))
    print(str(request.form))
    hostname = request.form.get('hostname', None)
    uid = request.form.get('uid', None)
    ip = request.form.get('ip', None)
    status = 200
    updateTime = request.form.get('updateTime', None) or time.ctime()
    info = request.form.get('info', None)
    print(hostname, uid, ip, status, updateTime, info)
    # return 'hello_world'
    if not(hostname and uid and ip and info):
        return json.dumps({'status': "fail"})
    if len(dbio.get(hostname)):
        dbio.update(hostname, uid, ip, status, updateTime, info)
    else:
        dbio.add(hostname, uid, ip, status, updateTime, info)

    # send to upstream servers
    if 'upstream_servers' in config and isinstance(config['upstream_servers'], list):
        data = dict(hostname=hostname, ip=ip, uid=uid, info=info)
        for server_url in config['upstream_servers']:
            try:
                response = requests.post(
                    server_url+'/host', data=data, timeout=2)
            except requests.exceptions.Timeout as e:
                print('upstream['+server_url+'] '+'TIMEOUT')
            else:
                print('upstream['+server_url+'] '+response.text)
                
    return json.dumps({'status': "success"})


@app.route('/test')
def test():
    return str(request.args['test'])


if __name__ == "__main__":
    app.run(debug=True)

    # conn = sqlite3.connect('test.db')
    # try:
    #     # create table
    #     cursor = conn.cursor()
    #     res = cursor.execute(SQL_CREATE_TABLE)
    #     print(res)
    #     conn.commit()

    #     app.run(host="0.0.0.0", port=8000)

    # finally:
    #     conn.close()
