from web3 import Web3

RPC_URL = 'http://localhost:8545'
# RPC_URL = 'https://mainnet.infura.io/v3/c60b0bb42f8a4c6481ecd229eddaca27'
w3 = Web3(Web3.HTTPProvider(RPC_URL))