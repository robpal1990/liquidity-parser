import json
import logging


def load_pool_cache():
    with open('pool_cache.json', 'r') as f:
        cache = json.load(f)
    return cache


CACHE = load_pool_cache()


def generate_swap_dag(events, transfers):
    swaps = []
    curve_v1_swaps = events.get('CURVE_V1')
    curve_v2_swaps = events.get('CURVE_V2')
    uni_v2_swaps = events.get('UNI_V2')
    uni_v3_swaps = events.get('UNI_V3', ()) + events.get('PANCAKE_V3', ())
    snx_swaps = events.get('SNX')
    integral_swaps = events.get('INTEGRAL')
    balancer_v2_swaps = events.get('BALANCER_V2')
    oneinch_rfq_swaps = events.get('ONEINCH_RFQ')
    dodo_swaps = events.get('DODO')
    dodo_v2_swaps = events.get('DODO_V2')
    psm_usdc_swaps = events.get('PSM_USDC')
    synapse_swaps = events.get('SYNAPSE')
    mav_v1_swaps = events.get('MAV_V1')
    bancor_swaps = events.get('BANCOR')
    defi_plaza_swaps = events.get('DEFI_PLAZA')

    reth_swaps = events.get('RETH')
    frxeth_swaps = events.get('FRXETH')

    rfq_order_swaps = events.get('RFQ_ORDER')
    bebop_rfq_swaps = events.get('BEBOP_RFQ')
    hashflow_swaps = events.get('HASHFLOW')
    clipper_swaps = events.get('CLIPPER')
    native_swaps = events.get('NATIVE_V1')

    if snx_swaps is not None:
        swaps += snx_swaps

    if reth_swaps is not None:
        swaps += reth_swaps

    if frxeth_swaps is not None:
        swaps += frxeth_swaps

    if oneinch_rfq_swaps is not None:
        swaps += oneinch_rfq_swaps

    if bebop_rfq_swaps is not None:
        swaps += bebop_rfq_swaps

    if native_swaps is not None:
        swaps += native_swaps

    if psm_usdc_swaps is not None:
        swaps += psm_usdc_swaps

    if hashflow_swaps is not None:
        swaps += hashflow_swaps

    if clipper_swaps is not None:
        swaps += clipper_swaps

    if rfq_order_swaps is not None:
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

    if synapse_swaps is not None:
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

    if dodo_v2_swaps is not None:
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

    if curve_v1_swaps is not None:
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

    if curve_v2_swaps is not None:
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

    if uni_v2_swaps is not None:
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
                continue

            if s['args']['amount0In'] > 0 and s['args']['amount1In'] == 0:
                swap['token_in'] = CACHE['UNI_V2'][s['address']]['0']
                swap['amount_in'] = s['args']['amount0In']
                swap['token_out'] = CACHE['UNI_V2'][s['address']]['1']
                swap['amount_out'] = s['args']['amount1Out']
            elif s['args']['amount1In'] > 0 and s['args']['amount0In'] == 0:
                swap['token_in'] = CACHE['UNI_V2'][s['address']]['1']
                swap['amount_in'] = s['args']['amount1In']
                swap['token_out'] = CACHE['UNI_V2'][s['address']]['0']
                swap['amount_out'] = s['args']['amount0Out']
            else:
                logging.warning('SUSPICIOUS UNI_V2 SWAP')
                continue
            swaps.append(swap)

    if uni_v3_swaps is not None:
        merged_cache = CACHE['PANCAKE_V3'] | CACHE['UNI_V3']
        for s in uni_v3_swaps:
            if s['address'] not in merged_cache:
                logging.warning(f"Missing UNI_V3/PANCAKE_V3 pool {s['address']}")
                continue

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

            if s['args']['amount0'] > 0 > s['args']['amount1']:
                swap['token_in'] = merged_cache[s['address']]['0']
                swap['amount_in'] = s['args']['amount0']
                swap['token_out'] = merged_cache[s['address']]['1']
                swap['amount_out'] = abs(s['args']['amount1'])
            elif s['args']['amount1'] > 0 > s['args']['amount0']:
                swap['token_in'] = merged_cache[s['address']]['1']
                swap['amount_in'] = s['args']['amount1']
                swap['token_out'] = merged_cache[s['address']]['0']
                swap['amount_out'] = abs(s['args']['amount0'])
            else:
                logging.warning('SUSPICIOUS UNI_V3 SWAP')
                continue
            swaps.append(swap)

    if balancer_v2_swaps is not None:
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

    if integral_swaps is not None:
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

    if dodo_swaps is not None:
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

    if mav_v1_swaps is not None:
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

    if bancor_swaps is not None:
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

    if defi_plaza_swaps is not None:
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

    return swaps
