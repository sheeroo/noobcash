from datetime import datetime
import inspect

class Colors:
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    INFO = '\033[36m'
    CLEAR = '\033[0m'
    
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
        fil = inspect.stack()[1].filename.split('/')[-1]
        fn = inspect.stack()[1].function
        print(Decoration.BOLD, f'[{now}]', Colors.WARNING, f'{fil}/{fn}()', Colors.CLEAR, Decoration.CLEAR)
        print(Decoration.UNDERLINE, header, Decoration.CLEAR)
        print(Colors.INFO, *args, Colors.CLEAR)

    @staticmethod
    def success(*args):
        fil = inspect.stack()[1].filename.split('/')[-1]
        fn = inspect.stack()[1].function
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
        print(Decoration.BOLD, f'[{now}]', Colors.WARNING, f'{fil}/{fn}()', Colors.CLEAR, Decoration.CLEAR)
        print(Colors.SUCCESS, *args, Colors.CLEAR)

    @staticmethod
    def warning(*args):
        fil = inspect.stack()[1].filename.split('/')[-1]
        fn = inspect.stack()[1].function
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
        print(Decoration.BOLD, f'[{now}]', Colors.WARNING, f'{fil}/{fn}()', Colors.CLEAR, Decoration.CLEAR)
        print(Colors.WARNING, *args, Colors.CLEAR)

    @staticmethod
    def error(*args):
        fil = inspect.stack()[1].filename.split('/')[-1]
        fn = inspect.stack()[1].function
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
        print(Decoration.BOLD, f'[{now}]', Colors.WARNING, f'{fil}/{fn}()', Colors.CLEAR, Decoration.CLEAR)
        print(Colors.ERROR, *args, Colors.CLEAR)
