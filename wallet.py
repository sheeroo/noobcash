import binascii

from Crypto import Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

class Wallet:

	def __init__(self, public_key, private_key):
		##set

		key = RSA.generate(2048)
		self.public_key = public_key or key.publickey().export_key(format = 'PEM')
		self.private_key = private_key or key.export_key(format = 'PEM')
		#self_address
		#self.transactions
	
	def balance(self):
		'''Returns:
            Int: the balance of the wallet
        '''
