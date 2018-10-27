import requests
import os
import json


hostname = os.popen('hostname').read().replace('\n', '')
with open("config.json") as f:
    obj = json.load(f)
    uid = obj['uid'] or "0"
    serverURL = obj['serverURL']
try:
    ip = requests.get("https://ifconfig.me", timeout=3)
except requests.exceptions.Timeout as e:
    ip = os.popen("ip addr | grep global  | sed 's/^[ \t]//g'  \
    |cut -f 5 -d ' '| head -n 1 ").read().replace('\n','')
info = os.popen('ip addr show | grep global').read().replace('\n', '')

data = dict(hostname=hostname, ip=ip, info=info, uid=uid)

try:
    response = requests.post(serverURL+'/host', data=data, timeout=5)
except requests.exceptions.Timeout as e:
    print("TIME OUT, server may not open")
print(response.text)
