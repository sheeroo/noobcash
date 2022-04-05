import uuid


class Utxo:
    def __init__(self, previous_trans_id, amount, recipient, id=None):
        self.id = id or uuid.uuid4().bytes.hex()
        self.previous_trans_id = previous_trans_id
        self.amount = amount
        self.recipient = recipient
    
    def to_dict(self):
        return dict(
            id=self.id,
            previous_trans_id=self.previous_trans_id,
            amount=self.amount,
            recipient=self.recipient
        )
    
    @staticmethod
    def from_dict(dictionary:dict):
        return Utxo(
            id=dictionary['id'],
            previous_trans_id=dictionary['previous_trans_id'],
            amount=dictionary['amount'],
            recipient=dictionary['recipient']
        )