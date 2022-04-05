from threading import Thread
import requests

from utils.debug import log

def broadcast(ring, url_action, data, responses, wait=False):
		'''Generic broadcast function using POST http method
		Args:
			url_action (String): Url to hit on other nodes,
			data (Dict): Dictionary to hit body
		Returns:
			array of responses
		'''
		threads=[]
		responses=[]
		def call_func(node, url_action, data, responses):
			log.info(f'Sending {data} to node {node.__str__()}...')
			response = requests.post(f'http://{node.ip}:{node.port}{url_action}', json=data)
			log.info(f'Responded with {response.text}...')
			responses.append(response)
		for node in ring:
			thread=Thread(target=call_func, args=(node, url_action, data, responses))
			threads.append(thread)
			thread.start()
		if not wait:
			return
		for thread in threads:
			thread.join()
		return responses