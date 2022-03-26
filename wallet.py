import binascii

#import Crypto
from Crypto import Random
#from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

class wallet:

	def __init__(self):
		key = RSA.generate(2048)
		self.public_key = key.publickey().export_key(format = 'PEM')
		self.private_key = key.export_key(format = 'PEM')
