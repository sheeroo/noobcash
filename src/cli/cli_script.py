from argparse import ArgumentParser
from urllib import request, response
import requests
from colorama import Fore
from time import sleep
from PyInquirer import prompt
import pyfiglet

IP = '0.0.0.0'

def client():

    print('\033[1m' + Fore.GREEN + 'Node initialized \n' + '\033[0m')
    
    while True:
        task = [{
            'type': 'list',
            'name': 'method',
            'message': 'Choose Task',
            'choices': ['Create Transaction', 'Show Transaction History', 'Show Balance', 'Help', 'Exit'],
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
                response = requests.post(address, json = transaction_a).json()
                print(response['message'])
            except requests.HTTPError as err:
                print(err)
            except Exception as e:
                print('ERROR')
                print(e)

        elif choice == 'show transaction history':
            print('\033[1m' + 'Completed Transactions from the Last Validated Block:' + '\033[0m')
            address = f'http://{IP}:{PORT}/transaction/view'
            try:
                response = requests.get(address).json()
                for r in response:
                    amount = r['amount']
                    receiver_address = r['receiver_address']
                    sender_address = r['sender_address']
                    print(f'User {sender_address} sent {amount} NBC to {receiver_address} \n')
            except Exception as e:
                print(e)
                print('Something went wrong\n') 

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

if __name__ == '__main__':     
    parser = ArgumentParser(description = 'CLI of noobcash')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-port', type = int, help = 'node port')

    args = parser.parse_args()
    PORT = args.port

    result = pyfiglet.figlet_format("NBC", font = "isometric1" )
    print(result)

    client()