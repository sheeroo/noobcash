from datetime import datetime

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
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
        print(Decoration.UNDERLINE, header)
        Decoration.clear()
        print('[', now, ']', Colors.INFO, *args)
        Colors.clear()
        Decoration.clear()

    @staticmethod
    def success(*args):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
        print('[', now, ']', Colors.SUCCESS, *args)
        Colors.clear()
        Decoration.clear()

    @staticmethod
    def warning(*args):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
        print('[', now, ']', Colors.WARNING, *args)
        Colors.clear()
        Decoration.clear()

    @staticmethod
    def error(*args):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
        print('[', now, ']', Colors.ERROR, *args)
        Colors.clear()
        Decoration.clear()
