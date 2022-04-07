from utils.debug import log
from .nbc import NbcException

class BlockException(NbcException):
    def __init__(self, block, message="This block is invalid"):
        self.message = message
        self.block = block
        log.error(self.__class__, ' -> ', message)
        super().__init__(self.message)

class InvalidBlockException(BlockException):
    def __init__(self, block, message="This block is invalid"):
        self.message = message
        super().__init__(block, self.message)

class AlreadyReceivedBlockException(BlockException):
    def __init__(self, block, message="This block has already been received"):
        super().__init__(block, message)
