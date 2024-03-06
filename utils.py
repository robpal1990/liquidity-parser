import json
import logging

from abis import UNI_V2, UNI_V3
from addresses import TOKENS
from web3_provider import w3

INVERTED_TOKENS = {v: k for k, v in TOKENS.items()}


def load_pool_cache():
    with open('pool_cache.json', 'r') as f:
        cache = json.load(f)
    return cache


CACHE = load_pool_cache()


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


def get_curve_v1_pool_data(address):
    pass


def generate_swap_dag(events, transfers, symbols):
    swaps = []
    curve_v1_swaps = events.get('CURVE_V1', [])
    curve_v2_swaps = events.get('CURVE_V2', [])
    uni_v2_swaps = events.get('UNI_V2', [])
    uni_v3_swaps = events.get('UNI_V3', ()) + events.get('PANCAKE_V3', ())  # Filthy
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
    defi_plaza_swaps = events.get('DEFI_PLAZA', [])
    mstable_swaps = events.get('MSTABLE', [])

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
            'token_in': CACHE['SYNAPSE'][s['address']][str(s['args']['soldId'])],
            'amount_in': s['args']['tokensSold'],
            'token_out': CACHE['SYNAPSE'][s['address']][str(s['args']['boughtId'])],
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
        if s['address'] not in CACHE['CURVE_V1']:
            logging.warning(f"Missing CURVE_V1 pool {s['address']}")
            continue

        swap = {
            'pool_address': s['address'],
            'protocol': 'curve_v1',
            'token_in': CACHE['CURVE_V1'][s['address']][str(s['args']['sold_id'])],
            'amount_in': s['args']['tokens_sold'],
            'token_out': CACHE['CURVE_V1'][s['address']][str(s['args']['bought_id'])],
            'amount_out': s['args']['tokens_bought'],
            'from': s['args']['buyer'],
            'to': s['args']['buyer'],
            'log_index': s['logIndex']
        }
        swaps.append(swap)

    for s in curve_v2_swaps:
        if s['address'] not in CACHE['CURVE_V2']:
            logging.warning(f"Missing CURVE_V2 pool {s['address']}")
            continue

        swap = {
            'pool_address': s['address'],
            'protocol': 'curve_v2',
            'token_in': CACHE['CURVE_V2'][s['address']][str(s['args']['sold_id'])],
            'amount_in': s['args']['tokens_sold'],
            'token_out': CACHE['CURVE_V2'][s['address']][str(s['args']['bought_id'])],
            'amount_out': s['args']['tokens_bought'],
            'from': s['args']['buyer'],
            'to': s['args']['buyer'],
            'log_index': s['logIndex']
        }
        swaps.append(swap)

    for s in uni_v2_swaps:
        swap = {
            'pool_address': s['address'],
            'protocol': 'uni_v2',
            'from': s['args']['sender'],
            'to': s['args']['to'],
            'log_index': s['logIndex']
        }

        if s['address'] not in CACHE['UNI_V2']:
            logging.warning(f"Missing UNI_V2 pool {s['address']}")
            logging.info(f"Fetching tokens for UNI_V3 pool {s['address']}")
            t0, t1 = get_uni_v2_pool_data(s['address'])
        else:
            t0 = CACHE['UNI_V2'][s['address']]['0']
            t1 = CACHE['UNI_V2'][s['address']]['1']

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
            logging.warning('SUSPICIOUS UNI_V2 SWAP')
            continue
        swaps.append(swap)

    merged_cache = CACHE['PANCAKE_V3'] | CACHE['UNI_V3']
    for s in uni_v3_swaps:
        swap = {
            'pool_address': s['address'],
            'from': s['args']['sender'],
            'to': s['args']['recipient'],
            'log_index': s['logIndex']
        }

        if 'protocolFeesToken0' in s['args']:
            swap['protocol'] = 'pancake_v3'
        else:
            swap['protocol'] = 'uni_v3'

        if s['address'] not in merged_cache:
            logging.warning(f"Missing UNI_V3/PANCAKE_V3 pool {s['address']}")
            logging.info(f"Fetching tokens for UNI_V3 pool {s['address']}")
            t0, t1 = get_uni_v3_pool_data(s['address'])
        else:
            t0 = merged_cache[s['address']]['0']
            t1 = merged_cache[s['address']]['1']

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
            logging.warning('SUSPICIOUS UNI_V3 SWAP')
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
        if s['address'] not in CACHE['DODO']:
            logging.warning(f"Missing DODO pool {s['address']}")
            continue

        swap = {
            'pool_address': s['address'],
            'protocol': 'dodo',
            'log_index': s['logIndex']
        }

        if s['event'] == 'BuyBaseToken':
            swap['token_in'] = CACHE['DODO'][s['address']]["1"]
            swap['amount_in'] = s['args']['payQuote']
            swap['token_out'] = CACHE['DODO'][s['address']]["0"]
            swap['amount_out'] = s['args']['receiveBase']
            swap['from'] = s['args']['buyer']
            swap['to'] = s['args']['buyer']
        elif s['event'] == 'SellBaseToken':
            swap['token_in'] = CACHE['DODO'][s['address']]["0"]
            swap['amount_in'] = s['args']['payBase']
            swap['token_out'] = CACHE['DODO'][s['address']]["1"]
            swap['amount_out'] = s['args']['receiveQuote']
            swap['from'] = s['args']['seller']
            swap['to'] = s['args']['seller']
        else:
            logging.warning('SUSPICIOUS DODO SWAP')
            continue
        swaps.append(swap)

    for s in mav_v1_swaps:
        if s['address'] not in CACHE['MAV_V1']:
            logging.warning(f"Missing MAV_V1 pool {s['address']}")
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
            swap['token_in'] = CACHE['MAV_V1'][s['address']]["0"]
            swap['token_out'] = CACHE['MAV_V1'][s['address']]["1"]
        else:
            swap['token_in'] = CACHE['MAV_V1'][s['address']]["1"]
            swap['token_out'] = CACHE['MAV_V1'][s['address']]["0"]
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

    # Filthy
    inverted = []
    if symbols:
        for s_ in swaps:
            symbol_in = INVERTED_TOKENS.get(s_['token_in'])
            if symbol_in is None:
                logging.warning(f"Unknown token {s_['token_in']}")
            else:
                s_['token_in'] = symbol_in
            symbol_out = INVERTED_TOKENS.get(s_['token_out'])
            if symbol_out is None:
                logging.warning(f"Unknown token {s_['token_out']}")
            else:
                s_['token_out'] = symbol_out
            inverted.append(s_)
        return inverted

    return swaps
