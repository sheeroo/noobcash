from collections import OrderedDict

import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import requests
import uuid
from flask import Flask, jsonify, request, render_template


class Transaction:

    def __init__(self, sender_address, sender_private_key, recipient_address, value, transaction_inputs):

        self.sender_address = sender_address
        self.receiver_address = recipient_address
        self.amount = value
        self.trans_uuid = uuid.uuid1().bytes
        self.transaction_id = SHA256.new(self.trans_uuid).hexdigest()
        self.transaction_inputs = transaction_inputs
        self.transaction_outputs = []
        self.signature = self.sign_transaction(sender_private_key)
        
    def sign_transaction(self, sender_private_key):
        """
        Sign transaction with private key
        """

        util = SHA256.new(self.trans_uuid)
        key = RSA.importKey(sender_private_key)
        signer = PKCS1_v1_5.new(key)
        signature = signer.new(util)

        return signature
        


       