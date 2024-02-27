STETH = [{
             "anonymous": False,
             "inputs": [],
             "name": "StakingPaused",
             "type": "event"}, {
             "anonymous": False,
             "inputs": [],
             "name": "StakingResumed",
             "type": "event"}, {
             "anonymous": False,
             "inputs": [{
                            "indexed": False,
                            "name": "maxStakeLimit",
                            "type": "uint256"}, {
                            "indexed": False,
                            "name": "stakeLimitIncreasePerBlock",
                            "type": "uint256"}],
             "name": "StakingLimitSet",
             "type": "event"}, {
             "anonymous": False,
             "inputs": [],
             "name": "StakingLimitRemoved",
             "type": "event"}, {
             "anonymous": False,
             "inputs": [{
                            "indexed": True,
                            "name": "reportTimestamp",
                            "type": "uint256"}, {
                            "indexed": False,
                            "name": "preCLValidators",
                            "type": "uint256"}, {
                            "indexed": False,
                            "name": "postCLValidators",
                            "type": "uint256"}],
             "name": "CLValidatorsUpdated",
             "type": "event"}, {
             "anonymous": False,
             "inputs": [{
                            "indexed": False,
                            "name": "depositedValidators",
                            "type": "uint256"}],
             "name": "DepositedValidatorsChanged",
             "type": "event"}, {
             "anonymous": False,
             "inputs": [{
                            "indexed": True,
                            "name": "reportTimestamp",
                            "type": "uint256"}, {
                            "indexed": False,
                            "name": "preCLBalance",
                            "type": "uint256"}, {
                            "indexed": False,
                            "name": "postCLBalance",
                            "type": "uint256"}, {
                            "indexed": False,
                            "name": "withdrawalsWithdrawn",
                            "type": "uint256"}, {
                            "indexed": False,
                            "name": "executionLayerRewardsWithdrawn",
                            "type": "uint256"}, {
                            "indexed": False,
                            "name": "postBufferedEther",
                            "type": "uint256"}],
             "name": "ETHDistributed",
             "type": "event"}, {
             "anonymous": False,
             "inputs": [{
                            "indexed": True,
                            "name": "reportTimestamp",
                            "type": "uint256"}, {
                            "indexed": False,
                            "name": "timeElapsed",
                            "type": "uint256"}, {
                            "indexed": False,
                            "name": "preTotalShares",
                            "type": "uint256"}, {
                            "indexed": False,
                            "name": "preTotalEther",
                            "type": "uint256"}, {
                            "indexed": False,
                            "name": "postTotalShares",
                            "type": "uint256"}, {
                            "indexed": False,
                            "name": "postTotalEther",
                            "type": "uint256"}, {
                            "indexed": False,
                            "name": "sharesMintedAsFees",
                            "type": "uint256"}],
             "name": "TokenRebased",
             "type": "event"}, {
             "anonymous": False,
             "inputs": [{
                            "indexed": False,
                            "name": "lidoLocator",
                            "type": "address"}],
             "name": "LidoLocatorSet",
             "type": "event"}, {
             "anonymous": False,
             "inputs": [{
                            "indexed": False,
                            "name": "amount",
                            "type": "uint256"}],
             "name": "ELRewardsReceived",
             "type": "event"}, {
             "anonymous": False,
             "inputs": [{
                            "indexed": False,
                            "name": "amount",
                            "type": "uint256"}],
             "name": "WithdrawalsReceived",
             "type": "event"}, {
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
             "type": "event"}, {
             "anonymous": False,
             "inputs": [{
                            "indexed": False,
                            "name": "amount",
                            "type": "uint256"}],
             "name": "Unbuffered",
             "type": "event"}, {
             "anonymous": False,
             "inputs": [{
                            "indexed": True,
                            "name": "executor",
                            "type": "address"}, {
                            "indexed": False,
                            "name": "script",
                            "type": "bytes"}, {
                            "indexed": False,
                            "name": "input",
                            "type": "bytes"}, {
                            "indexed": False,
                            "name": "returnData",
                            "type": "bytes"}],
             "name": "ScriptResult",
             "type": "event"}, {
             "anonymous": False,
             "inputs": [{
                            "indexed": True,
                            "name": "vault",
                            "type": "address"}, {
                            "indexed": True,
                            "name": "token",
                            "type": "address"}, {
                            "indexed": False,
                            "name": "amount",
                            "type": "uint256"}],
             "name": "RecoverToVault",
             "type": "event"}, {
             "anonymous": False,
             "inputs": [{
                            "indexed": False,
                            "name": "eip712StETH",
                            "type": "address"}],
             "name": "EIP712StETHInitialized",
             "type": "event"}, {
             "anonymous": False,
             "inputs": [{
                            "indexed": True,
                            "name": "from",
                            "type": "address"}, {
                            "indexed": True,
                            "name": "to",
                            "type": "address"}, {
                            "indexed": False,
                            "name": "sharesValue",
                            "type": "uint256"}],
             "name": "TransferShares",
             "type": "event"}, {
             "anonymous": False,
             "inputs": [{
                            "indexed": True,
                            "name": "account",
                            "type": "address"}, {
                            "indexed": False,
                            "name": "preRebaseTokenAmount",
                            "type": "uint256"}, {
                            "indexed": False,
                            "name": "postRebaseTokenAmount",
                            "type": "uint256"}, {
                            "indexed": False,
                            "name": "sharesAmount",
                            "type": "uint256"}],
             "name": "SharesBurnt",
             "type": "event"}, {
             "anonymous": False,
             "inputs": [],
             "name": "Stopped",
             "type": "event"}, {
             "anonymous": False,
             "inputs": [],
             "name": "Resumed",
             "type": "event"}, {
             "anonymous": False,
             "inputs": [{
                            "indexed": True,
                            "name": "from",
                            "type": "address"}, {
                            "indexed": True,
                            "name": "to",
                            "type": "address"}, {
                            "indexed": False,
                            "name": "value",
                            "type": "uint256"}],
             "name": "Transfer",
             "type": "event"}, {
             "anonymous": False,
             "inputs": [{
                            "indexed": True,
                            "name": "owner",
                            "type": "address"}, {
                            "indexed": True,
                            "name": "spender",
                            "type": "address"}, {
                            "indexed": False,
                            "name": "value",
                            "type": "uint256"}],
             "name": "Approval",
             "type": "event"}, {
             "anonymous": False,
             "inputs": [{
                            "indexed": False,
                            "name": "version",
                            "type": "uint256"}],
             "name": "ContractVersionSet",
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
    }
]