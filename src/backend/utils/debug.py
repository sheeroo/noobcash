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

    @staticmethod
    def clear():
        print('\u001b[0m')

class log:
    @classmethod
    def info(*args, header: str = ''):
        print(Decoration.UNDERLINE, header)
        Decoration.clear()
        print(Colors.INFO, Decoration.BOLD, *args)
        Colors.clear()
        Decoration.clear()

    @classmethod
    def success(*args):
        print(Colors.SUCCESS, Decoration.BOLD, *args)
        Colors.clear()
        Decoration.clear()

    @classmethod
    def warning(*args):
        print(Colors.WARNING, Decoration.BOLD, *args)
        Colors.clear()
        Decoration.clear()

    @classmethod
    def error(*args):
        print(Colors.ERROR, Decoration.BOLD, *args)
        Colors.clear()
        Decoration.clear()
