from exceptions.nbc import NbcException
from utils.debug import log

class TransactionException(NbcException):
    def __init__(self, transaction, message="There is an error with this transaction"):
        self.message = message
        self.transaction = transaction
        log.error(self.__class__, ' -> ', message)
        log.warning(self.transaction.transaction_id)
        super().__init__(self.message)

class InvalidTransactionException(TransactionException):
    def __init__(self, transaction, message="This transaction is invalid"):
        self.message = message
        super().__init__(transaction=transaction, message=self.message)
    
class InsufficientFundsException(TransactionException):
    def __init__(self, message="This transaction is invalid due to insufficient funds"):
        self.message = message
        log.error(self.__class__, ' -> ', message)