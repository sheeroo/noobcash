from threading import Thread
import requests
from utils.debug import log

def broadcast(ring, url_action, data, me = None, wait = False):
		'''Generic broadcast function using POST http method
		Args:
			ring (list(Node)): ring,
			url_action (String): Url to hit on other nodes,
			data (Dict): Dictionary to hit body,
			wait (boolean): Whether code should block and wait for threads to end to return responses
		Returns:
			array of responses
		'''
		threads=[]
		responses=[]
		def call_func(node, url_action, data):
			log.info(f'Sending data to node {node.ip}:{node.port}{url_action}...')
			response = requests.post(f'http://{node.ip}:{node.port}{url_action}', json=data, timeout=10)
			log.info(f'Node {node.ip}:{node.port} responded with {response.text}...')
			responses.append(response)
		for node in ring:
			if me != None and me.ip == node.ip and me.port == node.port:
				log.warning('PLEASE DONT SEND IT BACK TO ME')
				continue
			else:
				thread=Thread(target=call_func, args=(node, url_action, data))
				threads.append(thread)
				thread.start()
		if not wait:
			return None
		for thread in threads:
			thread.join()
		return responses