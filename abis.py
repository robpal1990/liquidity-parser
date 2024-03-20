AAVE_LENDING_V2 = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "reserve",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "user",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "onBehalfOf",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "uint16",
                "name": "referral",
                "type": "uint16"
            }
        ],
        "name": "Deposit",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "reserve",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "user",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "rateMode",
                "type": "uint256"
            }
        ],
        "name": "Swap",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "reserve",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "user",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "Withdraw",
        "type": "event"
    }
]

UNI_V2 = [{
    "constant": True,
    "inputs": [],
    "name": "token0",
    "outputs": [{
        "internalType": "address",
        "name": "",
        "type": "address"}],
    "payable": False,
    "stateMutability": "view",
    "type": "function"}, {
    "constant": True,
    "inputs": [],
    "name": "token1",
    "outputs": [{
        "internalType": "address",
        "name": "",
        "type": "address"}],
    "payable": False,
    "stateMutability": "view",
    "type": "function"},
    {
        "constant": True,
        "inputs": [],
        "name": "factory",
        "outputs": [{
            "internalType": "address",
            "name": "",
            "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"}]

UNI_V3 = [{
    "inputs": [],
    "name": "token0",
    "outputs": [{
        "internalType": "address",
        "name": "",
        "type": "address"}],
    "stateMutability": "view",
    "type": "function"}, {
    "inputs": [],
    "name": "token1",
    "outputs": [{
        "internalType": "address",
        "name": "",
        "type": "address"}],
    "stateMutability": "view",
    "type": "function"},
    {
        "inputs": [],
        "name": "factory",
        "outputs": [{
            "internalType": "address",
            "name": "",
            "type": "address"}],
        "stateMutability": "view",
        "type": "function"}]

UNI_V1 = [{
    "name": "tokenAddress",
    "outputs": [{
        "type": "address",
        "name": "out"}],
    "inputs": [],
    "constant": True,
    "payable": False,
    "type": "function",
    "gas": 1413}]

BALANCER_V2 = [{
    "inputs": [{
        "internalType": "bytes32",
        "name": "poolId",
        "type": "bytes32"}],
    "name": "getPoolTokens",
    "outputs": [{
        "internalType": "contract IERC20[]",
        "name": "tokens",
        "type": "address[]"}, {
        "internalType": "uint256[]",
        "name": "balances",
        "type": "uint256[]"}, {
        "internalType": "uint256",
        "name": "lastChangeBlock",
        "type": "uint256"}],
    "stateMutability": "view",
    "type": "function"}]
