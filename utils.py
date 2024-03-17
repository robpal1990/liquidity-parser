import json
import logging

import ipdb

from abis import UNI_V1, UNI_V2, UNI_V3
from data.logger import CustomFormatter
from token_abis import ERC20
from web3_provider import w3
from addresses import ETH, WETH


def load_token_cache():
    with open('data/token_cache.json', 'r') as f:
        cache = json.load(f)
    return cache


def save_token_cache(cache):
    with open('data/token_cache.json', 'w') as f:
        json.dump(cache, f, indent=4)


def load_pool_cache():
    with open('data/pool_cache.json', 'r') as f:
        cache = json.load(f)
    return cache


def save_pool_cache(cache):
    with open('data/pool_cache.json', 'w') as f:
        json.dump(cache, f, indent=4)


POOLS = load_pool_cache()
TOKENS = load_token_cache()

logger = logging.getLogger("DAG")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


def get_uni_v3_pool_data(address):
    pool = w3.eth.contract(address=address, abi=UNI_V3)
    t0 = pool.functions.token0().call()
    t1 = pool.functions.token1().call()
    return t0, t1


def get_uni_v2_pool_data(address):
    # Identical as v3
    pool = w3.eth.contract(address=address, abi=UNI_V2)
    t0 = pool.functions.token0().call()
    t1 = pool.functions.token1().call()
    return t0, t1


def get_uni_v1_pool_data(address):
    pool = w3.eth.contract(address=address, abi=UNI_V1)
    token = pool.functions.tokenAddress().call()
    return token


def get_curve_v1_pool_data(address):
    pass


def generate_swap_dag(events, transfers, symbols):
    swaps = []
    curve_v1_swaps = events.get('CURVE_V1', [])
    curve_v2_swaps = events.get('CURVE_V2', [])
    uni_v1_swaps = events.get('UNI_V1', [])
    uni_v2_swaps = events.get('UNI_V2', [])
    uni_v3_swaps = events.get('UNI_V3', [])
    pancake_v3_swaps = events.get('PANCAKE_V3', [])
    snx_swaps = events.get('SNX', [])
    integral_swaps = events.get('INTEGRAL', [])
    balancer_v1_swaps = events.get('BALANCER_V1', [])
    balancer_v2_swaps = events.get('BALANCER_V2', [])
    oneinch_rfq_swaps = events.get('ONEINCH_RFQ', [])
    oneinch_limit_swaps = events.get('ONEINCH_LIMIT', [])
    dodo_swaps = events.get('DODO', [])
    dodo_v2_swaps = events.get('DODO_V2', [])
    psm_usdc_swaps = events.get('PSM_USDC', [])
    synapse_swaps = events.get('SYNAPSE', [])
    mav_v1_swaps = events.get('MAV_V1', [])
    bancor_swaps = events.get('BANCOR', [])
    bancor_v3_swaps = events.get('BANCOR_V3', [])
    defi_plaza_swaps = events.get('DEFI_PLAZA', [])
    mstable_swaps = events.get('MSTABLE', [])
    kyber_swaps = events.get('KYBER', [])
    smoothy_v1_swaps = events.get('SMOOTHY_V1', [])
    fixed_rate_swaps = events.get('FIXED_RATE', [])

    reth_swaps = events.get('RETH', [])
    frxeth_swaps = events.get('FRXETH', [])

    rfq_order_swaps = events.get('RFQ_ORDER', [])
    bebop_rfq_swaps = events.get('BEBOP_RFQ', [])
    hashflow_swaps = events.get('HASHFLOW', [])
    clipper_swaps = events.get('CLIPPER', [])
    native_swaps = events.get('NATIVE_V1', [])
    steth_swaps = events.get('STETH', [])
    sdai_swaps = events.get('SDAI', [])

    swaps += snx_swaps
    swaps += mstable_swaps
    swaps += reth_swaps
    swaps += frxeth_swaps
    swaps += oneinch_rfq_swaps
    swaps += oneinch_limit_swaps
    swaps += bebop_rfq_swaps
    swaps += native_swaps
    swaps += psm_usdc_swaps
    swaps += hashflow_swaps
    swaps += clipper_swaps
    swaps += steth_swaps
    swaps += sdai_swaps

    for s in rfq_order_swaps:
        swap = {
            'pool_address': s['args']['maker'],
            'protocol': 'zeroex_rfq_order',
            'token_in': s['args']['takerToken'],
            'amount_in': s['args']['takerTokenFilledAmount'],
            'token_out': s['args']['makerToken'],
            'amount_out': s['args']['makerTokenFilledAmount'],
            'from': s['args']['taker'],
            'to': s['args']['taker'],
            'log_index': s['logIndex']
        }
        swaps.append(swap)

    for s in synapse_swaps:
        swap = {
            'pool_address': s['address'],
            'protocol': 'synapse',
            'token_in': POOLS['SYNAPSE'][s['address']][str(s['args']['soldId'])],
            'amount_in': s['args']['tokensSold'],
            'token_out': POOLS['SYNAPSE'][s['address']][str(s['args']['boughtId'])],
            'amount_out': s['args']['tokensBought'],
            'from': s['args']['buyer'],
            'to': s['args']['buyer'],
            'log_index': s['logIndex']
        }
        swaps.append(swap)

    for s in dodo_v2_swaps:
        swap = {
            'pool_address': s['address'],
            'protocol': 'dodo_v2',
            'token_in': s['args']['fromToken'],
            'amount_in': s['args']['fromAmount'],
            'token_out': s['args']['toToken'],
            'amount_out': s['args']['toAmount'],
            'from': s['args']['trader'],
            'to': s['args']['receiver'],
            'log_index': s['logIndex']
        }
        swaps.append(swap)

    for s in curve_v1_swaps:
        if s['address'] not in POOLS['CURVE_V1']:
            logger.warning(f"Missing CURVE_V1 pool {s['address']}")
            continue

        swap = {
            'pool_address': s['address'],
            'protocol': 'curve_v1',
            'token_in': POOLS['CURVE_V1'][s['address']][str(s['args']['sold_id'])],
            'amount_in': s['args']['tokens_sold'],
            'token_out': POOLS['CURVE_V1'][s['address']][str(s['args']['bought_id'])],
            'amount_out': s['args']['tokens_bought'],
            'from': s['args']['buyer'],
            'to': s['args']['buyer'],
            'log_index': s['logIndex']
        }
        swaps.append(swap)

    for s in curve_v2_swaps:
        if s['address'] not in POOLS['CURVE_V2']:
            logger.warning(f"Missing CURVE_V2 pool {s['address']}")
            continue

        swap = {
            'pool_address': s['address'],
            'protocol': 'curve_v2',
            'token_in': POOLS['CURVE_V2'][s['address']][str(s['args']['sold_id'])],
            'amount_in': s['args']['tokens_sold'],
            'token_out': POOLS['CURVE_V2'][s['address']][str(s['args']['bought_id'])],
            'amount_out': s['args']['tokens_bought'],
            'from': s['args']['buyer'],
            'to': s['args']['buyer'],
            'log_index': s['logIndex']
        }
        swaps.append(swap)

    for s in uni_v1_swaps:
        swap = {
            'pool_address': s['address'],
            'protocol': 'uni_v1',
            'from': s['args']['buyer'],
            'to': s['args']['buyer'],
            'log_index': s['logIndex']
        }

        if s['address'] not in POOLS['UNI_V1']:
            logger.warning(f"Missing UNI_V1 pool {s['address']}")
            t0 = get_uni_v1_pool_data(s['address'])
            t1 = ETH
            if t0 < WETH:
                POOLS['UNI_V1'][s['address']] = {
                    "0": t0,
                    "1": ETH}
            else:
                POOLS['UNI_V1'][s['address']] = {
                    "0": ETH,
                    "1": t0}
            save_pool_cache(POOLS)
        else:
            t0 = POOLS['UNI_V1'][s['address']]["0"]
            t1 = POOLS['UNI_V1'][s['address']]["1"]

        if t0 == ETH:
            token = t1
        else:
            token = t0

        if s['event'] == 'EthPurchase':
            swap['amount_in'] = s['args']['tokens_sold']
            swap['amount_out'] = s['args']['eth_bought']
            swap['token_in'] = token
            swap['token_out'] = ETH
        elif s['event'] == 'TokenPurchase':
            swap['amount_in'] = s['args']['eth_sold']
            swap['amount_out'] = s['args']['tokens_bought']
            swap['token_in'] = ETH
            swap['token_out'] = token
        else:
            logger.warning('SUSPICIOUS UNI_V1 SWAP')
            continue
        swaps.append(swap)

    for s in uni_v2_swaps:
        swap = {
            'pool_address': s['address'],
            'protocol': 'uni_v2',
            'from': s['args']['sender'],
            'to': s['args']['to'],
            'log_index': s['logIndex']
        }

        if s['address'] not in POOLS['UNI_V2']:
            logger.warning(f"Missing UNI_V2 pool {s['address']}")
            t0, t1 = get_uni_v2_pool_data(s['address'])
            POOLS['UNI_V2'][s['address']] = {
                "0": t0,
                "1": t1}
            save_pool_cache(POOLS)
        else:
            t0 = POOLS['UNI_V2'][s['address']]['0']
            t1 = POOLS['UNI_V2'][s['address']]['1']

        if s['args']['amount0In'] > 0 and s['args']['amount1In'] == 0:
            swap['token_in'] = t0
            swap['amount_in'] = s['args']['amount0In']
            swap['token_out'] = t1
            swap['amount_out'] = s['args']['amount1Out']
        elif s['args']['amount1In'] > 0 and s['args']['amount0In'] == 0:
            swap['token_in'] = t1
            swap['amount_in'] = s['args']['amount1In']
            swap['token_out'] = t0
            swap['amount_out'] = s['args']['amount0Out']
        else:
            logger.warning('SUSPICIOUS UNI_V2 SWAP')
            continue
        swaps.append(swap)

    for s in uni_v3_swaps:
        swap = {
            'pool_address': s['address'],
            'protocol': 'uni_v3',
            'from': s['args']['sender'],
            'to': s['args']['recipient'],
            'log_index': s['logIndex']
        }

        if s['address'] not in POOLS['UNI_V3']:
            logger.warning(f"Missing UNI_V3 pool {s['address']}")
            t0, t1 = get_uni_v3_pool_data(s['address'])
            POOLS['UNI_V3'][s['address']] = {
                "0": t0,
                "1": t1}
            save_pool_cache(POOLS)
        else:
            t0 = POOLS['UNI_V3'][s['address']]['0']
            t1 = POOLS['UNI_V3'][s['address']]['1']

        if s['args']['amount0'] > 0 > s['args']['amount1']:
            swap['token_in'] = t0
            swap['amount_in'] = s['args']['amount0']
            swap['token_out'] = t1
            swap['amount_out'] = abs(s['args']['amount1'])
        elif s['args']['amount1'] > 0 > s['args']['amount0']:
            swap['token_in'] = t1
            swap['amount_in'] = s['args']['amount1']
            swap['token_out'] = t0
            swap['amount_out'] = abs(s['args']['amount0'])
        else:
            logger.warning('SUSPICIOUS UNI_V3 SWAP')
            continue
        swaps.append(swap)

    for s in pancake_v3_swaps:
        swap = {
            'pool_address': s['address'],
            'protocol': 'pancake_v3',
            'from': s['args']['sender'],
            'to': s['args']['recipient'],
            'log_index': s['logIndex']
        }

        if s['address'] not in POOLS['PANCAKE_V3']:
            logger.warning(f"Missing PANCAKE_V3 pool {s['address']}")
            t0, t1 = get_uni_v3_pool_data(s['address'])
            POOLS['PANCAKE_V3'][s['address']] = {
                "0": t0,
                "1": t1}
            save_pool_cache(POOLS)

        else:
            t0 = POOLS['PANCAKE_V3'][s['address']]['0']
            t1 = POOLS['PANCAKE_V3'][s['address']]['1']

        if s['args']['amount0'] > 0 > s['args']['amount1']:
            swap['token_in'] = t0
            swap['amount_in'] = s['args']['amount0']
            swap['token_out'] = t1
            swap['amount_out'] = abs(s['args']['amount1'])
        elif s['args']['amount1'] > 0 > s['args']['amount0']:
            swap['token_in'] = t1
            swap['amount_in'] = s['args']['amount1']
            swap['token_out'] = t0
            swap['amount_out'] = abs(s['args']['amount0'])
        else:
            logger.warning('SUSPICIOUS UNI_V3 SWAP')
            continue
        swaps.append(swap)

    for s in balancer_v2_swaps:
        swap = {
            'pool_address': s['address'],
            'protocol': 'balancer_v2',
            'token_in': s['args']['tokenIn'],
            'amount_in': s['args']['amountIn'],
            'token_out': s['args']['tokenOut'],
            'amount_out': s['args']['amountOut'],
            'log_index': s['logIndex']
        }

        # Find matching transfers. Balancer V2 first emits, then moves funds.
        # Balancer multihops are just accounting inside the contract, no funds are moved
        # and will not emit Transfers.

        token_in_transfers = [t for t in transfers if
                              t['address'] == s['args']['tokenIn'] and t['args']['value'] == s['args'][
                                  'amountIn'] and
                              t[
                                  'logIndex'] > s['logIndex']]
        if len(token_in_transfers) > 0:
            token_in_transfer = token_in_transfers[0]
            swap['from'] = token_in_transfer['args']['from']
        token_out_transfers = [t for t in transfers if
                               t['address'] == s['args']['tokenOut'] and t['args']['value'] == s['args'][
                                   'amountOut'] and t[
                                   'logIndex'] > s['logIndex']]
        if len(token_out_transfers) > 0:
            token_out_transfer = token_out_transfers[0]
            swap['to'] = token_out_transfer['args']['to']

        # If no transfers then multihop within the Vault
        if swap.get('from') is None:
            swap['from'] = '0xBA12222222228d8Ba445958a75a0704d566BF2C8'
        if swap.get('to') is None:
            swap['to'] = '0xBA12222222228d8Ba445958a75a0704d566BF2C8'

        swaps.append(swap)

    for s in balancer_v1_swaps:
        swap = {
            'pool_address': s['address'],
            'protocol': 'balancer_v1',
            'token_in': s['args']['tokenIn'],
            'amount_in': s['args']['tokenAmountIn'],
            'token_out': s['args']['tokenOut'],
            'amount_out': s['args']['tokenAmountOut'],
            'from': s['args']['caller'],
            'to': s['args']['caller'],
            'log_index': s['logIndex']
        }
        swaps.append(swap)

    for s in integral_swaps:
        swap = {
            'pool_address': s['address'],
            'protocol': 'integral',
            'token_in': s['args']['tokenIn'],
            'amount_in': s['args']['amountIn'],
            'token_out': s['args']['tokenOut'],
            'amount_out': s['args']['amountOut'],
            'from': s['args']['sender'],
            'to': s['args']['to'],
            'log_index': s['logIndex']
        }
        swaps.append(swap)

    for s in dodo_swaps:
        if s['address'] not in POOLS['DODO']:
            logger.warning(f"Missing DODO pool {s['address']}")
            continue

        swap = {
            'pool_address': s['address'],
            'protocol': 'dodo',
            'log_index': s['logIndex']
        }

        if s['event'] == 'BuyBaseToken':
            swap['token_in'] = POOLS['DODO'][s['address']]["1"]
            swap['amount_in'] = s['args']['payQuote']
            swap['token_out'] = POOLS['DODO'][s['address']]["0"]
            swap['amount_out'] = s['args']['receiveBase']
            swap['from'] = s['args']['buyer']
            swap['to'] = s['args']['buyer']
        elif s['event'] == 'SellBaseToken':
            swap['token_in'] = POOLS['DODO'][s['address']]["0"]
            swap['amount_in'] = s['args']['payBase']
            swap['token_out'] = POOLS['DODO'][s['address']]["1"]
            swap['amount_out'] = s['args']['receiveQuote']
            swap['from'] = s['args']['seller']
            swap['to'] = s['args']['seller']
        else:
            logger.warning('SUSPICIOUS DODO SWAP')
            continue
        swaps.append(swap)

    for s in mav_v1_swaps:
        if s['address'] not in POOLS['MAV_V1']:
            logger.warning(f"Missing MAV_V1 pool {s['address']}")
            continue

        swap = {
            'pool_address': s['address'],
            'protocol': 'mav_v1',
            'log_index': s['logIndex'],
            # Simplification but seems like the `sender` address does not
            # take custody over tokens
            'from': s['args']['recipient'],
            'to': s['args']['recipient'],
            'amount_in': s['args']['amountIn'],
            'amount_out': s['args']['amountOut']

        }

        if s['args']['tokenAIn']:
            swap['token_in'] = POOLS['MAV_V1'][s['address']]["0"]
            swap['token_out'] = POOLS['MAV_V1'][s['address']]["1"]
        else:
            swap['token_in'] = POOLS['MAV_V1'][s['address']]["1"]
            swap['token_out'] = POOLS['MAV_V1'][s['address']]["0"]
        swaps.append(swap)

    for s in bancor_swaps:
        swap = {
            'pool_address': s['address'],
            'protocol': 'bancor',
            'token_in': s['args']['_fromToken'],
            'amount_in': s['args']['_amount'],
            'token_out': s['args']['_toToken'],
            'amount_out': s['args']['_return'],
            'from': s['args']['_trader'],
            'to': s['args']['_trader'],
            'log_index': s['logIndex']
        }
        swaps.append(swap)

    for s in bancor_v3_swaps:
        swap = {
            'pool_address': s['address'],
            'protocol': 'bancor_v3',
            'token_in': s['args']['sourceToken'],
            'amount_in': s['args']['sourceAmount'],
            'token_out': s['args']['targetToken'],
            'amount_out': s['args']['targetAmount'],
            'from': s['args']['trader'],
            'to': s['args']['trader'],
            'log_index': s['logIndex']
        }
        swaps.append(swap)

    for s in defi_plaza_swaps:
        swap = {
            'pool_address': s['address'],
            'protocol': 'defi_plaza',
            'token_in': s['args']['inputToken'],
            'amount_in': s['args']['inputAmount'],
            'token_out': s['args']['outputToken'],
            'amount_out': s['args']['outputAmount'],
            'from': s['args']['sender'],
            'to': s['args']['sender'],
            'log_index': s['logIndex']
        }
        swaps.append(swap)

    # Copypaste UNI V2
    for s in kyber_swaps:
        swap = {
            'pool_address': s['address'],
            'protocol': 'uni_v2',
            'from': s['args']['sender'],
            'to': s['args']['to'],
            'log_index': s['logIndex']
        }

        if s['address'] not in POOLS['KYBER']:
            logger.warning(f"Missing KYBER pool {s['address']}")
            t0, t1 = get_uni_v2_pool_data(s['address'])
            POOLS['KYBER'][s['address']] = {
                "0": t0,
                "1": t1}
            save_pool_cache(POOLS)
        else:
            t0 = POOLS['KYBER'][s['address']]['0']
            t1 = POOLS['KYBER'][s['address']]['1']

        if s['args']['amount0In'] > 0 and s['args']['amount1In'] == 0:
            swap['token_in'] = t0
            swap['amount_in'] = s['args']['amount0In']
            swap['token_out'] = t1
            swap['amount_out'] = s['args']['amount1Out']
        elif s['args']['amount1In'] > 0 and s['args']['amount0In'] == 0:
            swap['token_in'] = t1
            swap['amount_in'] = s['args']['amount1In']
            swap['token_out'] = t0
            swap['amount_out'] = s['args']['amount0Out']
        else:
            logger.warning('SUSPICIOUS KYBER SWAP')
            continue
        swaps.append(swap)

    for s in smoothy_v1_swaps:
        if s['address'] not in POOLS['SMOOTHY_V1']:
            logger.warning(f"Missing SMOOTHY_V1 pool {s['address']}")
            continue
        swap = {
            'pool_address': s['address'],
            'protocol': 'smoothy_v1',
            'token_in': POOLS['SMOOTHY_V1'][s['address']][str(s['args']['bTokenIdIn'])],
            'amount_in': s['args']['inAmount'],
            'token_out': POOLS['SMOOTHY_V1'][s['address']][str(s['args']['bTokenIdOut'])],
            'amount_out': s['args']['outAmount'],
            'from': s['args']['buyer'],
            'to': s['args']['buyer'],
            'log_index': s['logIndex']
        }
        swaps.append(swap)

    for s in fixed_rate_swaps:
        if s['address'] not in POOLS['FIXED_RATE']:
            logger.warning(f"Missing SMOOTHY_V1 pool {s['address']}")
            continue

        swap = {
            'pool_address': s['address'],
            'protocol': 'fixed_rate',
            'from': s['args']['trader'],
            'to': s['args']['trader'],
            'log_index': s['logIndex']
        }

        t0 = POOLS['FIXED_RATE'][s['address']]['0']
        t1 = POOLS['FIXED_RATE'][s['address']]['1']

        if s['args']['token0Amount'] > 0:
            swap['token_in'] = t0
            swap['amount_in'] = s['args']['token0Amount']
            swap['token_out'] = t1
            swap['amount_out'] = abs(s['args']['token1Amount'])
        elif s['args']['token1Amount'] > 0:
            swap['token_in'] = t1
            swap['amount_in'] = s['args']['token1Amount']
            swap['token_out'] = t0
            swap['amount_out'] = abs(s['args']['token0Amount'])
        else:
            logger.warning('SUSPICIOUS FIXED_RATE SWAP')
            continue
        import ipdb;
        ipdb.set_trace()
        swaps.append(swap)

    # Filthy
    swaps_with_symbols = []
    if symbols:
        for s_ in swaps:
            symbol_in = TOKENS.get(s_['token_in'], {}).get('symbol')
            if symbol_in is None:
                logger.warning(f"Unknown token {s_['token_in']}")
                token = w3.eth.contract(address=s_['token_in'], abi=ERC20)
                symbol = token.functions.symbol().call()
                decimals = token.functions.decimals().call()
                TOKENS[s_['token_in']] = {
                    "symbol": symbol,
                    "decimals": decimals}
                save_token_cache(TOKENS)
                logger.info(f"Added token {symbol} to cache")
                s_['token_in'] = symbol
            else:
                s_['token_in'] = symbol_in
            symbol_out = TOKENS.get(s_['token_out'], {}).get('symbol')
            if symbol_out is None:
                logger.warning(f"Unknown token {s_['token_out']}")
                token = w3.eth.contract(address=s_['token_out'], abi=ERC20)
                symbol = token.functions.symbol().call()
                decimals = token.functions.decimals().call()
                TOKENS[s_['token_out']] = {
                    "symbol": symbol,
                    "decimals": decimals}
                save_token_cache(TOKENS)
                logger.info(f"Added token {symbol} to cache")
                s_['token_out'] = symbol
            else:
                s_['token_out'] = symbol_out
            swaps_with_symbols.append(s_)
        return swaps_with_symbols

    return swaps
