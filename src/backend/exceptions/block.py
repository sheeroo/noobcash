from backend.classes.block import Block
from backend.exceptions.nbc import NbcException
from utils.debug import log

class BlockException(NbcException):
    def __init__(self, block:Block, message="This block is invalid"):
        self.message = message
        self.block = block
        log.error(self.__class__, ' -> ', message)
        log.warning(block.__repr__)
        super().__init__(self.message)

class InvalidBlockException(BlockException):
    def __init__(self, block: Block, message="This block is invalid"):
        self.message = message
        super().__init__(block, self.message)
    
