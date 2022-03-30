from collections import OrderedDict

import binascii
from shutil import ExecError

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
        self.trans_uuid = uuid.uuid4().bytes
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
    
    def verify_signature(self, sender, signature, transaction_id):
        '''Verification of a received transaction
		'''
        key = RSA.importKey(sender)
        util = SHA256.new(transaction_id)
        if PKCS1_v1_5.new(key).verify(util,key):
            raise Exception('Error in transaction verification')
        return 0


    def to_dict(self):
        return dict(
            sender_address = self.sender_address,
            receiver_address = self.receiver_address,
            amount = self.amount,
            trans_uuid = self.trans_uuid,
            transaction_id = self.transaction_id,
            transaction_inputs = self.transaction_inputs,
            transaction_outputs = self.transaction_outputs,
            signature = self.signature
        )

       