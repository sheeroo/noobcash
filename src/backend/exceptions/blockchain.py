from classes.block import Block
from exceptions.nbc import NbcException
from utils.debug import log

class BlockchainException(NbcException):
    def __init__(self, blockchain, message="This blockchain is invalid"):
        self.message = message
        self.blockchain = blockchain
        log.error(self.__class__, ' -> ', message)
        log.warning(self.blockchain.__str__())
        super().__init__(self.message)

class InvalidBlockchainException(BlockchainException):
    def __init__(self, blockchain, block: Block, message="This blockchain is invalid"):
        self.message = message
        self.block = block
        super().__init__(blockchain=blockchain, message=self.message)
    