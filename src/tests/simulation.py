from cProfile import run
import json
import os
import threading
import requests
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env

nodes = int(os.getenv('NODES'))
bootstrap_ip = os.getenv('BOOTSTRAP_IP')
bootstrap_port = int(os.getenv('BOOTSTRAP_PORT'))
result = requests.post(f'http://{bootstrap_ip}:{bootstrap_port}/state/get', json=None)
ring = result.json()['ring']
# print('RING', ring)

path = f'../../simulation/{nodes}nodes'
def run_simulation(node):
    ip = ring[node]['ip']
    port = ring[node]['port']
    print('IP:', ip)
    print('PORT:', port)
    with open(f'{path}/transactions{node}.txt','r',encoding = 'utf-8') as f:
        for line in f:
            arguments = line.split(' ')
            receiver = arguments[0][2]
            amount = arguments[1]
            print(f'({threading.get_ident()}) -> Node {node} is sending {amount} NBC to node {receiver}')
            data = dict(
                receiver=int(receiver),
                amount=int(amount)
            )
            response = requests.post(f'http://{ip}:{port}/transaction/create', json=data)
            print(json.dumps(response.json(), indent=4))

threads = []
for i in range(nodes):
    thread = threading.Thread(target=run_simulation, args=(i,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()