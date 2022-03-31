class Colors:
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    INFO = '\033[36m'
    
    @staticmethod
    def clear():
        print('\033[0m')

class Decoration:
    BOLD = '\u001b[1m'
    UNDERLINE = '\u001b[4m'
    REVERSED = '\u001b[7m'
    CLEAR = '\u001b[0m'

    @staticmethod
    def clear():
        print('\u001b[0m')

class log:
    @staticmethod
    def info(*args, header: str = ''):
        print(Decoration.UNDERLINE, header)
        Decoration.clear()
        print(Colors.INFO, *args)
        Colors.clear()
        Decoration.clear()

    @staticmethod
    def success(*args):
        print(Colors.SUCCESS, *args)
        Colors.clear()
        Decoration.clear()

    @staticmethod
    def warning(*args):
        print(Colors.WARNING, *args)
        Colors.clear()
        Decoration.clear()

    @staticmethod
    def error(*args):
        print(Colors.ERROR, *args)
        Colors.clear()
        Decoration.clear()
