# coding=utf-8
#!/usr/bin/python3

from cpc_fusion import Web3
from solc import compile_source
from cpc_fusion.contract import ConciseContract

# the failure of calling creat_contract may be due to a low gas value
# adding gas may solve the problem

url = 'http://localhost:8501'

# web3.py instance
w3 = Web3(Web3.HTTPProvider(url))

# set pre-funded account as sender
w3.cpc.defaultAccount = w3.cpc.accounts[0]

# change the keypath to your keystore file
keypath = "/Users/huangqinghao/Workspace/Hackathons/BitRun9102/workspace/employee2/keystore/UTC--2019-04-20T04-45-24.347359000Z--8f73f5fd17279250902fcb5da778e9682c9de0f8"
password = "hqh941218"
filepath = "time_track.txt"
# account_addr = '0xc6aba3e25a1a8e7f0445fca321d1ffc3dcd61e3f'
account_addr = '0x8f73f5fd17279250902fcb5da778e9682c9de0f8'
# contract_addr = "0x3Df0aFfeA5Ee45d17e06955d1FD55A335C880828"
contract_addr = "0xE3212eb1CD24fb168f0D81Bb695a69676f4a36B9"


def get_contract_interface(filepath, contract_name):
    contract_code_file = open(filepath,"r")
    contract_source_code = contract_code_file.read()
    compiled_sol = compile_source(contract_source_code)  # Compiled source code
    contract_interface = compiled_sol[f'<stdin>:{contract_name}']

    return contract_interface

contract_interface = get_contract_interface(filepath, 'TimeTrack')
timeTrack = w3.cpc.contract(
    address=contract_addr,
    abi=contract_interface['abi'],
)

def creat_contract(filepath,contract_name,keypath,password,account_addr):
    # Solidity source code
    contract_code_file = open(filepath,"r")
    contract_source_code = contract_code_file.read()
    print(contract_source_code)
    compiled_sol = compile_source(contract_source_code)  # Compiled source code
    contract_interface = compiled_sol[f'<stdin>:{contract_name}']


    # Instantiate and deploy contract
    Greeter = w3.cpc.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

    # Submit the transaction that deploys the contract
    from_addr = w3.toChecksumAddress(account_addr)
    tx_hash = Greeter.constructor().raw_transact({
        # Increase or decrease gas according to contract conditions
        'gas': 3000000,
        'from': from_addr,
        'value': 0
    }, keypath, password, 42)

    print('*********', w3.cpc.getTransactionReceipt(tx_hash))

    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.cpc.waitForTransactionReceipt(tx_hash)
    # tx_receipt1 = w3.cpc.waitForTransactionReceipt(tx_hash_raw)
    print(tx_receipt)
    # print(tx_receipt1)

    # Create the contract instance with the newly-deployed address
    greeter = w3.cpc.contract(
        address=tx_receipt.contractAddress,
        abi=contract_interface['abi'],
    )
    return greeter,w3,tx_receipt.contractAddress

def callPunchIn():
    w3 = Web3(Web3.HTTPProvider(url))
    from_addr = w3.toChecksumAddress(account_addr)
    tx_hash = timeTrack.functions.doPunchIN().raw_transact({
        'gas': 300000,
        'from':from_addr,
        'value': 0,
    },keypath,password,42)
    # Wait for transaction to be mined...
    w3.cpc.waitForTransactionReceipt(tx_hash)
    print(
        tx_hash
    )
    return timeTrack.functions.getEmployees().call()

def call_contract():
    # cpc_fusion.cpc.getTransactionReceipt()
    w3 = Web3(Web3.HTTPProvider(url))
    from_addr = w3.toChecksumAddress(account_addr)
    # add employee
    # tx_hash = contract.functions.addEmployee().raw_transact({
    #     'gas': 340000,
    #     'from':from_addr,
    #     'value': 0,
    # },keypath,password,42)
    
    # w3.cpc.waitForTransactionReceipt(tx_hash)

    # # punchin
    # tx_hash = contract.functions.doPunchIN().raw_transact({
    #     'gas': 340000,
    #     'from':from_addr,
    #     'value': 0,
    # },keypath,password,42)

    # # Wait for transaction to be mined...
    # w3.cpc.waitForTransactionReceipt(tx_hash)
    
    print(
        timeTrack.functions.getEmployees().call()
    )
    return timeTrack.functions.getEmployees().call()

if __name__ == '__main__':

    # creat_contract(filepath,'TimeTrack',keypath,password,account_addr)
    call_contract()