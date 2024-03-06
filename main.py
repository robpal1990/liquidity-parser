import json
import logging
import warnings
from collections import defaultdict
from pprint import pprint

import pandas as pd
from web3_provider import w3

from abis import AAVE_LENDING_V2
from addresses import TOKENS, ZERO, PSM_USDC_A, CLIPPER_POOL
from swap_event_abis import BALANCER_V1, BALANCER_V2, UNI, UNI_V2, UNI_V3, CURVE_V1, CURVE_V2, CURVE_V2_1, PANCAKE_V3, \
    SYNAPSE, BANCOR, BANCOR_V3, KYBER, MAV_V1, DODO, DODO_V2, CLIPPER, OTC_ORDER, RFQ_ORDER, HASHFLOW, ONEINCH_RFQ, \
    ONEINCH_LIMIT, INTEGRAL, SNX, BEBOP_RFQ, NATIVE_V1, DEFI_PLAZA, MSTABLE
from token_abis import STETH, RETH, SFRXETH, AAVE_TOKEN, ERC20
from utils import generate_swap_dag

warnings.filterwarnings("ignore")

logging.getLogger("web3").setLevel(logging.CRITICAL)

BALANCER_V1 = w3.eth.contract(address=None, abi=BALANCER_V1)
BALANCER_V2 = w3.eth.contract(address=None, abi=BALANCER_V2)  # Also SWAAP_V2
DODO = w3.eth.contract(address=None, abi=DODO)
DODO_V2 = w3.eth.contract(address=None, abi=DODO_V2)
UNI = w3.eth.contract(address=None, abi=UNI)
UNI_V2 = w3.eth.contract(address=None, abi=UNI_V2)  # Also: SUSHI, SHIBA, CRO, NOMISWAP, PANCAKE, FRAXSWAP, SAKESWAP
UNI_V3 = w3.eth.contract(address=None, abi=UNI_V3)  # Also: KYBER_ELASTIC, SOLIDLY_V3
PANCAKE_V3 = w3.eth.contract(address=None, abi=PANCAKE_V3)
CURVE_V1 = w3.eth.contract(address=None, abi=CURVE_V1)
CURVE_V2 = w3.eth.contract(address=None, abi=CURVE_V2)
CURVE_V2_1 = w3.eth.contract(address=None, abi=CURVE_V2_1)
SYNAPSE = w3.eth.contract(address=None, abi=SYNAPSE)
BANCOR_V3 = w3.eth.contract(address=None, abi=BANCOR_V3)
BANCOR = w3.eth.contract(address=None, abi=BANCOR)
KYBER = w3.eth.contract(address=None, abi=KYBER)
DEFI_PLAZA = w3.eth.contract(address=None, abi=DEFI_PLAZA)
MSTABLE = w3.eth.contract(address=None, abi=MSTABLE)
MAV_V1 = w3.eth.contract(address=None, abi=MAV_V1)
CLIPPER = w3.eth.contract(address=None, abi=CLIPPER)
OTC_ORDER = w3.eth.contract(address=None, abi=OTC_ORDER)
HASHFLOW = w3.eth.contract(address=None, abi=HASHFLOW)
RFQ_ORDER = w3.eth.contract(address=None, abi=RFQ_ORDER)
ONEINCH_RFQ = w3.eth.contract(address=None, abi=ONEINCH_RFQ)
ONEINCH_LIMIT = w3.eth.contract(address=None, abi=ONEINCH_LIMIT)
BEBOP_RFQ = w3.eth.contract(address=None, abi=BEBOP_RFQ)
NATIVE_V1 = w3.eth.contract(address=None, abi=NATIVE_V1)
INTEGRAL = w3.eth.contract(address=None, abi=INTEGRAL)
SNX = w3.eth.contract(address=None, abi=SNX)


def load_pool_cache():
    with open('pool_cache.json', 'r') as f:
        cache = json.load(f)
    return cache


CACHE = load_pool_cache()


def get_oneinch_rfq(r_):
    token = w3.eth.contract(address=None, abi=ERC20)
    rfq_events = ONEINCH_RFQ.events.OrderFilledRFQ().process_receipt(r_)
    transfers = token.events.Transfer().process_receipt(r_)
    rfq = []
    for event in rfq_events:
        index = event['logIndex']
        # Last two transfers before OrderFilledRFQ should be the swap
        last_two = [e for e in transfers if e['logIndex'] < index][-2:]
        in_, out_ = last_two[0], last_two[1]
        maker, maker_token, maker_amount = in_['args']['from'], in_['address'], in_['args']['value']
        taker, taker_token, taker_amount = out_['args']['from'], out_['address'], out_['args']['value']
        rfq_action = {
            'pool_address': maker,
            'protocol': 'oneinch_rfq',
            'token_out': maker_token,
            'amount_out': maker_amount,
            'token_in': taker_token,
            'amount_in': taker_amount,
            'from': out_['args']['from'],
            'to': in_['args']['to'],
            'log_index': index
        }
        rfq.append(rfq_action)
    return rfq


def get_oneinch_limit(r_):
    token = w3.eth.contract(address=None, abi=ERC20)
    limit_events = ONEINCH_LIMIT.events.OrderFilled().process_receipt(r_)
    transfers = token.events.Transfer().process_receipt(r_)
    limit = []
    for event in limit_events:
        index = event['logIndex']
        maker = event['args']['maker']
        # Next two token transfers should have
        next_two = [e for e in transfers if e['logIndex'] > index]
        in_, out_ = next_two[0], next_two[1]
        if not (in_['args']['from'] == out_['args']['to'] or in_['args']['to'] == out_['args']['from']):
            continue
        assert len(next_two) >= 2
        maker, maker_token, maker_amount = in_['args']['from'], in_['address'], in_['args']['value']
        taker, taker_token, taker_amount = out_['args']['from'], out_['address'], out_['args']['value']
        limit_action = {
            'pool_address': maker,
            'protocol': 'oneinch_limit',
            'token_out': maker_token,
            'amount_out': maker_amount,
            'token_in': taker_token,
            'amount_in': taker_amount,
            'from': out_['args']['from'],
            'to': in_['args']['to'],
            'log_index': index
        }
        limit.append(limit_action)
    return limit


def get_bebop_rfq(r_):
    token = w3.eth.contract(address=None, abi=ERC20)
    rfq_events = BEBOP_RFQ.events.AggregateOrderExecuted().process_receipt(r_)
    transfers = token.events.Transfer().process_receipt(r_)
    rfq = []
    for event in rfq_events:
        index = event['logIndex']
        # Last two transfers before AggregateOrderExecuted should be the swap
        last_two = [e for e in transfers if e['logIndex'] < index][-2:]
        in_, out_ = last_two[0], last_two[1]
        maker, maker_token, maker_amount = in_['args']['from'], in_['address'], in_['args']['value']
        taker, taker_token, taker_amount = out_['args']['from'], out_['address'], out_['args']['value']
        rfq_action = {
            'pool_address': maker,
            'protocol': 'bebop_rfq',
            'token_out': maker_token,
            'amount_out': maker_amount,
            'token_in': taker_token,
            'amount_in': taker_amount,
            'from': out_['args']['from'],
            'to': in_['args']['to'],
            'log_index': index
        }
        rfq.append(rfq_action)
    return rfq


def get_hashflow_rfq(r_):
    token = w3.eth.contract(address=None, abi=ERC20)
    rfq_events = HASHFLOW.events.Trade().process_receipt(r_)
    transfers = token.events.Transfer().process_receipt(r_)
    rfq = []
    for event in rfq_events:
        previous = [e for e in transfers if e['logIndex'] < event['logIndex']][-1]
        next_ = [e for e in transfers if e['logIndex'] > event['logIndex']][0]
        assert next_['args']['from'] == previous['args']['to']
        rfq_action = {
            'pool_address': next_['args']['from'],
            'protocol': 'hashflow',
            'token_in': event['args']['baseToken'],
            'amount_in': event['args']['baseTokenAmount'],
            'token_out': event['args']['quoteToken'],
            'amount_out': event['args']['quoteTokenAmount'],
            'from': event['args']['trader'],
            'to': event['args']['trader'],
            'log_index': event['logIndex']
        }
        rfq.append(rfq_action)
    return rfq


def get_native_rfq(r_):
    token = w3.eth.contract(address=None, abi=ERC20)
    rfq_events = NATIVE_V1.events.SwapCalculations().process_receipt(r_)
    transfers = token.events.Transfer().process_receipt(r_)
    rfq = []
    for event in rfq_events:
        next_two = [e for e in transfers if e['logIndex'] > event['logIndex']][:2]
        amount_in = event['args']['amountIn']
        assert next_two[1]['args']['value'] == amount_in
        rfq_action = {
            'pool_address': next_two[0]['args']['from'],
            'protocol': 'native_v1',
            'token_in': next_two[1]['address'],
            'amount_in': next_two[1]['args']['value'],
            'token_out': next_two[0]['address'],
            'amount_out': next_two[0]['args']['value'],
            'from': event['args']['recipient'],
            'to': event['args']['recipient'],
            'log_index': event['logIndex']
        }
        rfq.append(rfq_action)
    return rfq


def get_clipper_actions(r_):
    token = w3.eth.contract(address=None, abi=ERC20)
    swap_events = CLIPPER.events.Swapped().process_receipt(r_)
    transfers = token.events.Transfer().process_receipt(r_)
    swaps = []
    for s in swap_events:
        previous = [e for e in transfers if e['logIndex'] < s['logIndex']
                    and e['args']['to'] == CLIPPER_POOL][-1]
        swap = {
            'pool_address': s['address'],
            'protocol': 'clipper',
            'token_in': s['args']['inAsset'],
            'amount_in': s['args']['inAmount'],
            'token_out': s['args']['outAsset'],
            'amount_out': s['args']['outAmount'],
            'from': previous['args']['from'],
            'to': s['args']['recipient'],
            'log_index': s['logIndex']
        }
        swaps.append(swap)
    return swaps


def get_mstable_actions(r_):
    # This greatly oversimplifies mStable interactions
    # Can have Compound, Aave, Synthetix actions inside
    token = w3.eth.contract(address=None, abi=ERC20)
    # Swapped() events don't have the amount_in...
    # Probably buggy, trying to find the matching transfer (one before last?)
    swap_events = MSTABLE.events.Swapped().process_receipt(r_)
    transfers = token.events.Transfer().process_receipt(r_)
    swaps = []
    for s in swap_events:
        swap = {
            'pool_address': s['address'],
            'protocol': 'mstable',
            'token_in': s['args']['input'],
            'token_out': s['args']['output'],
            'amount_out': s['args']['outputAmount'],
            'from': s['args']['swapper'],
            'to': s['args']['recipient'],
            'log_index': s['logIndex']
        }
        previous = [e for e in transfers if e['logIndex'] < s['logIndex']
                    and e['address'] == swap['token_in']]

        assert len(previous) >= 2

        swap['amount_in'] = previous[-2]['args']['value']
        swaps.append(swap)
    return swaps


def get_aave_actions(r_):
    first_log_index = r_['logs'][0]['logIndex']
    pool = w3.eth.contract(address=None, abi=AAVE_LENDING_V2)
    atoken = w3.eth.contract(address=None, abi=AAVE_TOKEN)
    aave_deposits = pool.events.Deposit().process_receipt(r_)
    aave_withdrawals = pool.events.Withdraw().process_receipt(r_)

    mints = []
    for deposit in aave_deposits:
        from_ = deposit['args']['onBehalfOf']
        index = deposit['logIndex']
        mint_log = atoken.events.Mint().process_log(r_['logs'][index - 1 - first_log_index])
        assert mint_log['args']['from'] == from_
        mint_action = {
            'address': from_,
            'token_deposited': deposit['args']['reserve'],
            'token_minted': mint_log['address'],
            'deposit_amount': deposit['args']['amount'],
            'mint_amount': mint_log['args']['value'],
            'log_index': index
        }
        mints.append(mint_action)

    burns = []
    for withdrawal in aave_withdrawals:
        from_ = withdrawal['args']['user']
        index = withdrawal['logIndex']
        burn_log = atoken.events.Burn().process_log(r_['logs'][index - 1 - first_log_index])
        assert burn_log['args']['from'] == from_
        mint_action = {
            'address': from_,
            'token_withdrawn': withdrawal['args']['reserve'],
            'token_burned': burn_log['address'],
            'withdrawal_amount': withdrawal['args']['amount'],
            'burn_amount': burn_log['args']['value'],
            'log_index': index
        }
        burns.append(mint_action)
    return {
        'mints': mints,
        'burns': burns
    }


def get_steth_actions(r_):
    first_log_index = r_['logs'][0]['logIndex']
    token = w3.eth.contract(address=TOKENS['stETH'], abi=STETH)
    transfers = token.events.Transfer().process_receipt(r_)

    steth_wraps = [t for t in transfers if
                   t.address == TOKENS['stETH'] and t['args'][
                       'to'] == TOKENS['wstETH']]
    actions = []
    for wrap in steth_wraps:
        from_ = wrap['args']['from']
        index = wrap['logIndex']
        previous = [e for e in transfers if e['logIndex'] < wrap['logIndex']
                    and e['address'] == TOKENS['wstETH']]
        assert len(previous) > 0
        wsteth_log = previous[-1]
        assert wsteth_log['args']['to'] == from_
        wrap_action = {
            'pool_address': TOKENS['wstETH'],
            'from': from_,
            'to': from_,
            'protocol': 'steth_wrap',
            'token_in': TOKENS['stETH'],
            'amount_in': wrap['args']['value'],
            'token_out': TOKENS['wstETH'],
            'amount_out': wsteth_log['args']['value'],
            'log_index': index
        }
        actions.append(wrap_action)

    steth_unwraps = [t for t in transfers if
                     t.address == TOKENS['stETH'] and t['args'][
                         'from'] == TOKENS['wstETH']]

    for unwrap in steth_unwraps:
        to_ = unwrap['args']['to']
        index = unwrap['logIndex']
        previous = [e for e in transfers if e['logIndex'] < unwrap['logIndex']
                    and e['address'] == TOKENS['wstETH']]
        assert len(previous) > 0
        wsteth_log = previous[-1]
        assert wsteth_log['args']['from'] == to_
        wrap_action = {
            'pool_address': TOKENS['wstETH'],
            'from': to_,
            'to': to_,
            'protocol': 'steth_unwrap',
            'token_in': TOKENS['wstETH'],
            'amount_in': wsteth_log['args']['value'],
            'token_out': TOKENS['stETH'],
            'amount_out': unwrap['args']['value'],
            'log_index': index
        }
        actions.append(wrap_action)

    steth_mints = [t for t in transfers if
                   t.address == TOKENS['stETH'] and t['args'][
                       'from'] == ZERO]
    for mint in steth_mints:
        to_ = mint['args']['to']
        deposits = token.events.Submitted().process_receipt(r_)
        prev_deposits = [d for d in deposits if d['logIndex'] < mint['logIndex']]
        assert len(prev_deposits) > 0
        deposit_log = prev_deposits[-1]
        assert deposit_log['address'] == TOKENS['stETH']
        assert deposit_log['args']['sender'] == to_
        mint_action = {
            'pool_address': TOKENS['stETH'],
            'from': to_,
            'to': to_,
            'protocol': 'steth_mint',
            'token_in': TOKENS['WETH'],
            'amount_in': deposit_log['args']['amount'],
            'token_out': TOKENS['stETH'],
            'amount_out': mint['args']['value'],
            'log_index': mint['logIndex']
        }
        actions.append(mint_action)

    return actions


def get_snx_actions(r_):
    actions = SNX.events.AtomicSynthExchange().process_receipt(r_)
    swaps = []
    for s_ in actions:
        from_token = s_['args']['fromCurrencyKey'].decode("utf-8").rstrip('\x00')
        to_token = s_['args']['toCurrencyKey'].decode("utf-8").rstrip('\x00')
        from_address = TOKENS.get(from_token)
        to_address = TOKENS.get(to_token)
        if from_address is None:
            logging.info(f"Missing token {from_address}")
        if to_address is None:
            logging.info(f"Missing token {to_address}")
        swap = {
            'pool_address': s_['address'],
            'token_in': from_address,
            'amount_in': s_['args']['fromAmount'],
            'token_out': to_address,
            'amount_out': s_['args']['toAmount'],
            'from': s_['args']['account'],
            'to': s_['args']['toAddress'],
            'protocol': 'snx',
            'log_index': s_['logIndex']
        }
        swaps.append(swap)
    return swaps


def get_psm_usdc_actions(r_):
    erc20 = w3.eth.contract(address=None, abi=ERC20)
    transfers = erc20.events.Transfer().process_receipt(r_)

    swaps = []
    usdc_to_psm = [t for t in transfers if t['address'] == TOKENS['USDC']
                   and t['args']['to'] == PSM_USDC_A]
    for u in usdc_to_psm:
        dai_mints = [t for t in transfers if t['logIndex'] - 5 == u['logIndex']
                     and t['args']['from'] == ZERO
                     # and t['args']['to'] == u['args']['from']
                     ]

        assert len(dai_mints) > 0
        next_mint = dai_mints[0]
        swap = {
            'pool_address': PSM_USDC_A,
            'protocol': 'psm_usdc_dai',
            'token_in': TOKENS['USDC'],
            'amount_in': u['args']['value'],
            'token_out': TOKENS['DAI'],
            'amount_out': next_mint['args']['value'],
            'from': u['args']['from'],
            'to': next_mint['args']['to'],
            'log_index': u['logIndex']
        }
        swaps.append(swap)

    usdc_from_psm = [t for t in transfers if t['address'] == TOKENS['USDC']
                     and t['args']['from'] == PSM_USDC_A]
    for u in usdc_from_psm:
        dai_burns = [t for t in transfers if t['logIndex'] == u['logIndex'] - 4
                     # and t['args']['from'] == u['args']['to']
                     and t['args']['to'] == ZERO]

        assert len(dai_burns) > 0
        prev_burn = dai_burns[-1]
        swap = {
            'pool_address': PSM_USDC_A,
            'protocol': 'psm_usdc_dai',
            'token_in': TOKENS['DAI'],
            'amount_in': prev_burn['args']['value'],
            'token_out': TOKENS['USDC'],
            'amount_out': u['args']['value'],
            'from': prev_burn['args']['from'],
            'to': u['args']['to'],
            'log_index': u['logIndex']
        }
        swaps.append(swap)

    return swaps


def get_frxeth_actions(r_):
    token = w3.eth.contract(address=TOKENS['sfrxETH'], abi=SFRXETH)
    deposits = token.events.Deposit().process_receipt(r_)
    deposits = [d for d in deposits if d['address'] == TOKENS['sfrxETH']]
    withdrawals = token.events.Withdraw().process_receipt(r_)
    withdrawals = [w for w in withdrawals if w['address'] == TOKENS['sfrxETH']]
    swaps = []
    for d in deposits:
        action = {
            'pool_address': TOKENS['sfrxETH'],
            'protocol': 'sfrxeth_mint',
            'token_in': TOKENS['frxETH'],
            'amount_in': d['args']['assets'],
            'token_out': TOKENS['sfrxETH'],
            'amount_out': d['args']['shares'],
            # TODO: Make sure it's the caller
            'from': d['args']['caller'],
            'to': d['args']['owner'],
            'log_index': d['logIndex']
        }
        swaps.append(action)
    for w in withdrawals:
        action = {
            'pool_address': TOKENS['sfrxETH'],
            'protocol': 'sfrxeth_burn',
            'token_in': TOKENS['sfrxETH'],
            'amount_in': w['args']['shares'],
            'token_out': TOKENS['frxETH'],
            'amount_out': w['args']['assets'],
            # TODO: Make sure it's the caller
            'from': w['args']['caller'],
            'to': w['args']['receiver'],
            'log_index': w['logIndex']
        }
        swaps.append(action)
    return swaps


def get_sdai_actions(r_):
    token = w3.eth.contract(address=TOKENS['sfrxETH'], abi=SFRXETH)
    deposits = token.events.Deposit().process_receipt(r_)
    deposits = [d for d in deposits if d['address'] == '0x83F20F44975D03b1b09e64809B757c47f942BEeA']
    # withdrawals = token.events.Withdraw().process_receipt(r_)
    # withdrawals = [w for w in withdrawals if w['address'] == '0x83F20F44975D03b1b09e64809B757c47f942BEeA']
    swaps = []
    for d in deposits:
        action = {
            'pool_address': '0x83F20F44975D03b1b09e64809B757c47f942BEeA',
            'protocol': 'sdai_mint',
            'token_in': TOKENS['DAI'],
            'amount_in': d['args']['assets'],
            'token_out': '0x83F20F44975D03b1b09e64809B757c47f942BEeA',
            'amount_out': d['args']['shares'],
            # TODO: Make sure it's the caller
            'from': d['args']['caller'],
            'to': d['args']['owner'],
            'log_index': d['logIndex']
        }
        swaps.append(action)
    return swaps


def get_reth_actions(r_):
    token = w3.eth.contract(address=TOKENS['rETH'], abi=RETH)
    burns = token.events.TokensBurned().process_receipt(r_)
    # TODO: Mints?
    swaps = []
    for b in burns:
        action = {
            'pool_address': TOKENS['rETH'],
            'protocol': 'reth_burn',
            'token_in': TOKENS['rETH'],
            'amount_in': b['args']['amount'],
            'token_out': TOKENS['WETH'],
            'amount_out': b['args']['ethAmount'],
            'from': b['args']['from'],
            'to': b['args']['from'],
            'log_index': b['logIndex']
        }
        swaps.append(action)

    return swaps


def get_mkusd_actions(r_):
    # 0x1b75c69fb1e599ce4067b772d79bf926a98f4f2e409c83817a53567b2bdbb9c1
    pass


# def get_sdai_actions(r_):
#     # 0x0c067dc4d141e2476eed2653d99c840e9537daac3363dc94eb2d489719658f24
#     pass


def extract_erc20_transfers(receipt):
    erc20 = w3.eth.contract(address=None, abi=ERC20)
    transfers = erc20.events.Transfer().process_receipt(receipt)
    return transfers


def tally_dag(dag):
    """
    Check the token tallies to see if we are missing
    a swap. Net flows of all intermediate tokens should
    be near zero.
    """

    tally = defaultdict(int)
    for d in dag:
        if d['token_in'] == '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE':
            tally['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'] += d['amount_in']
        elif d['token_in'] == 'ETH':
            tally['WETH'] += d['amount_in']
        else:
            tally[d['token_in']] += d['amount_in']

        if d['token_out'] == '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE':
            tally['0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'] -= d['amount_out']
        elif d['token_out'] == 'ETH':
            tally['WETH'] -= d['amount_in']
        else:
            tally[d['token_out']] -= d['amount_out']
    return tally


def extract_swaps(r):
    swap_events = {
        'BALANCER_V1': BALANCER_V1.events.LOG_SWAP().process_receipt(r),
        'BALANCER_V2': BALANCER_V2.events.Swap().process_receipt(r),
        'DODO': DODO.events.SellBaseToken().process_receipt(r) + DODO.events.BuyBaseToken().process_receipt(r),
        'DODO_V2': DODO_V2.events.DODOSwap().process_receipt(r),
        'UNI': UNI.events.TokenPurchase().process_receipt(r),
        'UNI_V2': UNI_V2.events.Swap().process_receipt(r),
        'UNI_V3': UNI_V3.events.Swap().process_receipt(r),
        'PANCAKE_V3': PANCAKE_V3.events.Swap().process_receipt(r),
        'CURVE_V1': CURVE_V1.events.TokenExchange().process_receipt(
            r) + CURVE_V1.events.TokenExchangeUnderlying().process_receipt(r),
        'CURVE_V2': CURVE_V2.events.TokenExchange().process_receipt(
            r) + CURVE_V2_1.events.TokenExchange().process_receipt(r),
        'SYNAPSE': SYNAPSE.events.TokenSwap().process_receipt(r),
        'BANCOR_V3': BANCOR_V3.events.TokensTraded().process_receipt(r),
        'BANCOR': BANCOR.events.Conversion().process_receipt(r),
        'KYBER': KYBER.events.Swap().process_receipt(r),
        'DEFI_PLAZA': DEFI_PLAZA.events.Swapped().process_receipt(r),
        'MSTABLE': get_mstable_actions(r),
        'MAV_V1': MAV_V1.events.Swap().process_receipt(r),
        'OTC_ORDER': OTC_ORDER.events.OtcOrderFilled().process_receipt(r),
        'HASHFLOW': get_hashflow_rfq(r),
        'RFQ_ORDER': RFQ_ORDER.events.RfqOrderFilled().process_receipt(r),
        'INTEGRAL': INTEGRAL.events.Sell().process_receipt(r) + INTEGRAL.events.Buy().process_receipt(r),
        'SNX': get_snx_actions(r),
        'ONEINCH_RFQ': get_oneinch_rfq(r),
        'ONEINCH_LIMIT': get_oneinch_limit(r),
        'BEBOP_RFQ': get_bebop_rfq(r),
        'CLIPPER': get_clipper_actions(r),
        'PSM_USDC': get_psm_usdc_actions(r),
        'RETH': get_reth_actions(r),
        'FRXETH': get_frxeth_actions(r),
        'NATIVE_V1': get_native_rfq(r),
        'STETH': get_steth_actions(r),
        'SDAI': get_sdai_actions(r)
    }

    # aave_actions = get_aave_actions(r)
    # swap_events['AAVE_ACTIONS'] = get_aave_actions(r)

    return {k: v for k, v in swap_events.items() if v}


def main():
    logging.info('Loading data')
    data = pd.read_csv('/home/robert/Projects/liquidity-parser/1inch_agg.csv')
    # logging.info('Data loaded')
    cache = load_pool_cache()
    pools_cached = set([k for v in cache.values() for k in v.keys()])

    # Weird metapool events: https://etherscan.io/tx/0x48a571b2e7a842a0c0a1981433de9e7e582bf6ad3f6adc217439afcca451c178
    # receipt = w3.eth.get_transaction_receipt('0xa2ba7939818d920aef9d1b2e1222d4df962ac30610367c0ec67c3a0fb3c5dbbc') Cowswap DAO
    receipt = w3.eth.get_transaction_receipt('0xbfbaa8826d89ced9b2e150cd19c00920ccee4e0ad6f0ba74ba61f9544e617ae4')
    transfers = extract_erc20_transfers(receipt)
    swaps = extract_swaps(receipt)
    dag = generate_swap_dag(swaps, transfers, symbols=True)
    logging.info(f"Protocols used:{list(swaps.keys())}")
    pprint(dag)
    pprint(dict(tally_dag(dag)))
    import ipdb;
    ipdb.set_trace()

    for i, r in data.iterrows():
        if i < 130:
            continue
        tx_hash = r['tx_hash']
        logging.info(f"Processing transaction {i}: {tx_hash}")
        receipt = w3.eth.get_transaction_receipt(r['tx_hash'])
        swaps = extract_swaps(receipt)
        transfers = extract_erc20_transfers(receipt)
        dag = generate_swap_dag(swaps, transfers, symbols=True)
        logging.info(f"Protocols used:{swaps.keys()}")
        pprint(dict(tally_dag(dag)))

    import ipdb;
    ipdb.set_trace()


if __name__ == '__main__':
    logging.basicConfig(encoding='utf-8', level=logging.INFO)
    main()
