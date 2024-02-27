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

PSM = [
    {
        "anonymous": True,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes4",
                "name": "sig",
                "type": "bytes4"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "usr",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "arg1",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "arg2",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "data",
                "type": "bytes"
            }
        ],
        "name": "LogNote",
        "type": "event"
    }
]


