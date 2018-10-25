from sanic import Sanic 
from sanic.response import json
import time
import sqlite3

SQL_CREATE_TABLE = "create TABLE IF NOT EXISTS myIP \
(hostname text,ip text, status text,updateTime text,info text)"

app = Sanic()

@app.route("/")
async def test(request):
    print(request)
    return json({"hello":"world"})

@app.route("/hosts")
async def test(request):
    print(request.args)
    return json({"e":1})
    

if __name__ == "__main__":
    
    conn = sqlite3.connect('test.db')
    try:
        # create table
        cursor = conn.cursor()
        res = cursor.execute(SQL_CREATE_TABLE)
        print(res)
        conn.commit()

        app.run(host="0.0.0.0", port=8000)

    finally: 
        conn.close()