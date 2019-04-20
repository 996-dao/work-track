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
keypath = "/Users/huangqinghao/Workspace/Hackathons/BitRun9102/workspace/employee11/keystore/UTC--2019-04-20T18-41-24.962422000Z--faf1a023d6d9bfd96564c7547420a0b3b8c61076"
password = "123123"
filepath = "time_track.txt"
account_addr = '0xfaf1a023d6d9bfd96564c7547420a0b3b8c61076'
contract_addr = "0xD5fC25C575eD7c834007FD5B5472C8f6E13bbcEB"


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

def creat_contract():
    # Instantiate and deploy contract
    Contract = w3.cpc.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    # Submit the transaction that deploys the contract
    from_addr = w3.toChecksumAddress(account_addr)
    tx_hash = Contract.constructor().raw_transact({
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

    return tx_receipt.contractAddress

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
    return timeTrack.functions.displayPunchTime().call()

def callPunchOut():
    w3 = Web3(Web3.HTTPProvider(url))
    from_addr = w3.toChecksumAddress(account_addr)
    tx_hash = timeTrack.functions.doPunchOUT().raw_transact({
        'gas': 300000,
        'from':from_addr,
        'value': 0,
    },keypath,password,42)
    # Wait for transaction to be mined...
    w3.cpc.waitForTransactionReceipt(tx_hash)
    return timeTrack.functions.getEmployees().call()


def callAddEmployee():
    w3 = Web3(Web3.HTTPProvider(url))
    from_addr = w3.toChecksumAddress(account_addr)
    tx_hash = timeTrack.functions.addEmployee().raw_transact({
        'gas': 300000,
        'from':from_addr,
        'value': 0,
    },keypath,password,42)
    # Wait for transaction to be mined...
    w3.cpc.waitForTransactionReceipt(tx_hash)
    return timeTrack.functions.getEmployees().call()

def call_contract():
    w3 = Web3(Web3.HTTPProvider(url))
    from_addr = w3.toChecksumAddress(account_addr)
    print(
        timeTrack.functions.getEmployees().call()
    )
    return timeTrack.functions.getEmployees().call()

def call_displayMe():
    w3 = Web3(Web3.HTTPProvider(url))
    from_addr = w3.toChecksumAddress(account_addr)
    print(
        timeTrack.functions.displayMyOvertimeCount().call()
    )
    print(
        timeTrack.functions.displayMyPunchDayNum().call()
    )
    print(
        timeTrack.functions.displayMyPunchStatus().call()
    )
    print(
        timeTrack.functions.displayMyAddr().call()
    )
    return timeTrack.functions.displayMyOvertimeCount().call()

def call_display_global():
    w3 = Web3(Web3.HTTPProvider(url))
    from_addr = w3.toChecksumAddress(account_addr)
    print(
        timeTrack.functions.displayTotalPunchInCount().call()
    )
    print(
        timeTrack.functions.displayTotalPunchOutCount().call()
    )
    print(
        timeTrack.functions.displayTotalOvertimeCount().call()
    )
    print(
        timeTrack.functions.displayCurrentMsgSender().call()
    )

    print(
        timeTrack.functions.displayCurrentEmployeeAddress().call()
    )
    print(
        timeTrack.functions.getFirstEmployeeEntityAddress().call()
    )

    return timeTrack.functions.displayTotalOvertimeCount().call()

if __name__ == '__main__':

    # creat_contract()
    # callAddEmployee()
    # call_contract()
    # callPunchIn()
    # callPunchOut()
    call_display_global()
    call_displayMe()