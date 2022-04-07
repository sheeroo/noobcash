from argparse import ArgumentParser
from audioop import add
from urllib import request, response
import requests
from colorama import Fore
from time import sleep
from prompt_toolkit import prompt

IP = '127.0.0.1'

def client():

    print('\033[1m' + Fore.GREEN + 'Node initialized \n' + '\033[0m')
    
    while True:
        task = [{
            'name': 'method',
            'message': 'Choose Task',
            'menu': ['Create Transaction', 'Show Transaction History', 'Show Balance', 'Help', 'Exit'],
            'filter': lambda val: val.lower()
        }]

        choice = prompt(task)['method']
    
        if choice =='create transaction':
            print('Creating New Transaction')
            transaction_q = [{
                    'type': 'input',
                    'name': 'receiver',
                    'message': "Receiver (type receiver's id):",
                    'filter': lambda val: int(val)
                },
                {
                    'type': 'input',
                    'name': 'amount',
                    'message': 'Amount:',
                    'filter': lambda val: int(val)
                }]
            
            transaction_a = prompt(transaction_q)
            address = f'http://{IP}:{PORT}/transaction/create'
            try:
                response = requests.post(add, data = transaction_a).json()
                print(f'Transfering {response["amount"]} NBCs to {response["receiver"]}\n')
            except:
                print('Something went wrong\n')

        elif choice == 'show transaction history':
            raise Exception('Not Implemented Yet')
        elif choice == 'show balance':
            print('\033[1m' + 'Current Balance:' + '\033[0m')
            address = f'http://{IP}:{PORT}/balance'
            try:
                response = requests.get(address).json()
                print(f'{response["balance"]} NBCs\n')
            except:
                print('Something went wrong\n')
        elif choice == 'help':
            print('\033[1m' + '--------- HELP ---------\n' + '\033[0m')
            print('Menu:\n')
            print('- "Create Transaction": Create a new transaction by specifying the receiver node id and the amount of NBCs you would like to send')
            print('- "Show Transaction History": Display past completed transactions of the last block')
            print('- "Show Balance": Display current wallet balance')
            print('- "Exit": Exit cli')
            print('\033[1m' + '------------------------\n' + '\033[0m')
        elif choice == 'exit':
            break
        else:
            print('Type help to see the availialbe options\n')

if __name__ == 'main':     
    parser = ArgumentParser(description = 'CLI of noobcash')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-port', type = int, help = 'node port')

    args = parser.parse_args()
    PORT = args.port

    client()