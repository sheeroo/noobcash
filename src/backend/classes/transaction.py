from collections import OrderedDict

import binascii
import json
from shutil import ExecError
import time

import Crypto
import Crypto.Random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import requests
import uuid
from classes.utxo import Utxo

from exceptions.transaction import InvalidTransactionException
from utils.debug import log

class Transaction:
    def __init__(
        self, 
        sender_address, 
        receiver_address, 
        amount, 
        transaction_inputs,
        sender_private_key: str = None, 
        transaction_outputs=None, 
        signature=None, 
        transaction_id=None,
        trans_uuid=None,
        timestamp=None
    ):
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.amount = amount
        self.trans_uuid = trans_uuid or transaction_id or uuid.uuid4().bytes
        self.transaction_id = transaction_id or SHA256.new(self.trans_uuid).hexdigest() #hexnumber
        self.transaction_inputs: list(Utxo) = transaction_inputs
        self.transaction_outputs = transaction_outputs or []
        self.signature = signature or self.sign_transaction(sender_private_key)
        self.timestamp = timestamp or time.time()
        
    def sign_transaction(self, sender_private_key):
        """
        Sign transaction with private key
        """

        util = SHA256.new(self.trans_uuid)
        key = RSA.importKey(sender_private_key)
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(util)

        return signature
    
    def verify_signature(self):
        '''Verification of a received transaction
		'''
        key = RSA.importKey(self.sender_address)
        util = SHA256.new(self.trans_uuid)
        if PKCS1_v1_5.new(key).verify(util, self.signature):
            log.success('Transaction verified: ' + self.__str__())
            return True
        else:
            raise InvalidTransactionException(transaction=self, message='Error in transaction verification')

    def calculate_outputs(self):
        total = 0
        for utxo in self.transaction_inputs:
            #already validated so I'm just adding bro
            total += utxo.amount
        
        # Receiver utxo
        receiver_utxo = Utxo(
            previous_trans_id=self.transaction_id,
            amount=self.amount,
            recipient=self.receiver_address
        )
        
        sender_utxo = Utxo(
            previous_trans_id=self.transaction_id,
            amount=total - self.amount, #RESTA
            recipient=self.sender_address.decode()
        )
        transaction_outputs = [receiver_utxo, sender_utxo]
        self.transaction_outputs = transaction_outputs
        
        return transaction_outputs

# Everything is serialized except sender's private key
    def to_dict(self):
        transaction_inputs = [Utxo.to_dict(ti) for ti in self.transaction_inputs]
        transaction_outputs = [Utxo.to_dict(to) for to in self.transaction_outputs]
        return dict(
            sender_address = self.sender_address.decode(),
            receiver_address = self.receiver_address,
            amount = self.amount,
            transaction_id = self.transaction_id,
            trans_uuid = self.trans_uuid.decode(encoding="ISO-8859-1"),
            transaction_inputs = transaction_inputs,
            transaction_outputs = transaction_outputs,
            signature = self.signature.decode(encoding="ISO-8859-1"),
            timestamp = self.timestamp
        )

    @staticmethod
    def from_dict(dictionary: dict):
        transaction_inputs = [Utxo.from_dict(ti) for ti in dictionary['transaction_inputs']]
        transaction_outputs = [Utxo.from_dict(to) for to in dictionary['transaction_outputs']]
        return Transaction(
            sender_address=dictionary['sender_address'].encode(),
            receiver_address=dictionary['receiver_address'],
            amount=dictionary['amount'],
            transaction_id=dictionary['transaction_id'],
            trans_uuid = dictionary['trans_uuid'].encode(encoding="ISO-8859-1"),
            transaction_inputs=transaction_inputs,
            transaction_outputs=transaction_outputs,
            signature = dictionary['signature'].encode(encoding="ISO-8859-1"),
            timestamp=dictionary['timestamp']
        )

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)

    def __repr__(self):
        return self.amount + ' NBC from ' + self.sender_address + ' to ' + self.receiver_address + self.transaction_inputs + ' at ' + self.timestamp  