from threading import Thread
import requests

def broadcast(ring, url_action, data, responses):
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
			response = requests.post(f'{node.ip}:{node.port}/{url_action}', data=data)
			responses.append(response)
		for node in ring:
			thread=Thread(target=call_func, args=(node, url_action, data, responses))
			threads.append(thread)
			thread.start()

		for thread in threads:
			thread.join()
		return responses