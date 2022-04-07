import os
import requests
import logging
import sys
import threading
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env
root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

nodes_no = int(os.getenv('NODES'))
if not nodes_no:
    exit(0)

responses = []
def call_node(ip, port, action, data=None, method=None):
    logging.info(f'Sending http://{ip}:{port}{action} data {data}')
    if method == 'POST' or method == None:
        response = requests.post(f'http://{ip}:{port}{action}', json=data)
    elif method == 'GET':
        response = requests.get(f'http://{ip}:{port}{action}')
    
    responses.append(response)
    logging.info(f'http://{ip}:{port}{action} responded with {response.text}')
    return responses

responses = []
threads = []
index = 0
for i in range(nodes_no):
    thread=threading.Thread(target=call_node, args=('127.0.0.1', 5000 + index, '/balance', None, 'GET'))
    index += 1
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()

for r in responses:
    print(r.json())