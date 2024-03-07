STETH = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "to",
                "type": "address"},
            {
                "indexed": False,
                "name": "sharesValue",
                "type": "uint256"
            }
        ],
        "name": "TransferShares",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [{
            "indexed": True,
            "name": "sender",
            "type": "address"}, {
            "indexed": False,
            "name": "amount",
            "type": "uint256"}, {
            "indexed": False,
            "name": "referral",
            "type": "address"}],
        "name": "Submitted",
        "type": "event"}
]

RETH = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "time",
                "type": "uint256"
            }
        ],
        "name": "EtherDeposited",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "ethAmount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "time",
                "type": "uint256"
            }
        ],
        "name": "TokensBurned",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
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
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "ethAmount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "time",
                "type": "uint256"
            }
        ],
        "name": "TokensMinted",
        "type": "event"
    }
]

SFRXETH = [{
    "anonymous": False,
    "inputs": [{
        "indexed": True,
        "internalType": "address",
        "name": "caller",
        "type": "address"}, {
        "indexed": True,
        "internalType": "address",
        "name": "owner",
        "type": "address"}, {
        "indexed": False,
        "internalType": "uint256",
        "name": "assets",
        "type": "uint256"}, {
        "indexed": False,
        "internalType": "uint256",
        "name": "shares",
        "type": "uint256"}],
    "name": "Deposit",
    "type": "event"}, {
    "anonymous": False,
    "inputs": [{
        "indexed": True,
        "internalType": "address",
        "name": "caller",
        "type": "address"}, {
        "indexed": True,
        "internalType": "address",
        "name": "receiver",
        "type": "address"}, {
        "indexed": True,
        "internalType": "address",
        "name": "owner",
        "type": "address"}, {
        "indexed": False,
        "internalType": "uint256",
        "name": "assets",
        "type": "uint256"}, {
        "indexed": False,
        "internalType": "uint256",
        "name": "shares",
        "type": "uint256"}],
    "name": "Withdraw",
    "type": "event"}]

AAVE_TOKEN = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "target",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "index",
                "type": "uint256"
            }
        ],
        "name": "Burn",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "index",
                "type": "uint256"
            }
        ],
        "name": "Mint",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
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
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    }
]

ERC20 = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{
                        "name": "",
                        "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"}
]
