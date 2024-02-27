from web3 import Web3

EVENTS = {
    '0xddf252ad': 'Transfer',
    '0x8c5be1e5': 'Approval'
}


def get_log_selector(log):
    # contract = log.address
    topic0 = log.topics[0]
    selector = topic0[:4].hex()
    return selector
