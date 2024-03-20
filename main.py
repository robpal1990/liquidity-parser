import json
import logging
import warnings
from collections import defaultdict
from pprint import pprint

import pandas as pd

from data.logger import CustomFormatter
from web3_provider import w3

from abis import AAVE_LENDING_V2
from addresses import TOKENS, ZERO, PSM_USDC_A, CLIPPER_POOL, AGG_ROUTER_V5, AGG_ROUTER_V6, wstETH, stETH, WETH
from swap_event_abis import BALANCER_V1, BALANCER_V2, UNI_V1, UNI_V2, UNI_V3, CURVE_V1, CURVE_V2, CURVE_V2_1, \
    PANCAKE_V3, \
    SYNAPSE, BANCOR, BANCOR_V3, KYBER, MAV_V1, DODO, DODO_V2, CLIPPER, OTC_ORDER, RFQ_ORDER, HASHFLOW, ONEINCH_RFQ, \
    ONEINCH_V5_LIMIT, ONEINCH_V6_LIMIT, INTEGRAL, SNX, BEBOP_RFQ, NATIVE_V1, DEFI_PLAZA, MSTABLE, SMOOTHY_V1, \
    FIXED_RATE, SMARDEX
from token_abis import STETH, RETH, SFRXETH, AAVE_TOKEN, ERC20
from utils import generate_swap_dag

warnings.filterwarnings("ignore")

logger = logging.getLogger("WEB3")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

BALANCER_V1 = w3.eth.contract(address=None, abi=BALANCER_V1)
BALANCER_V2 = w3.eth.contract(address=None, abi=BALANCER_V2)  # Also SWAAP_V2
DODO = w3.eth.contract(address=None, abi=DODO)
DODO_V2 = w3.eth.contract(address=None, abi=DODO_V2)
UNI_V1 = w3.eth.contract(address=None, abi=UNI_V1)
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
ONEINCH_V5_LIMIT = w3.eth.contract(address=None, abi=ONEINCH_V5_LIMIT)
ONEINCH_V6_LIMIT = w3.eth.contract(address=None, abi=ONEINCH_V6_LIMIT)
BEBOP_RFQ = w3.eth.contract(address=None, abi=BEBOP_RFQ)
NATIVE_V1 = w3.eth.contract(address=None, abi=NATIVE_V1)
INTEGRAL = w3.eth.contract(address=None, abi=INTEGRAL)
SNX = w3.eth.contract(address=None, abi=SNX)
SMOOTHY_V1 = w3.eth.contract(address=None, abi=SMOOTHY_V1)
FIXED_RATE = w3.eth.contract(address=None, abi=FIXED_RATE)
SMARDEX = w3.eth.contract(address=None, abi=SMARDEX)


def load_pool_cache():
    with open('data/pool_cache.json', 'r') as f:
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
    # MIGHT BE BROKEN FOR 1INCH FUSION
    token = w3.eth.contract(address=None, abi=ERC20)
    v5_limit_events = ONEINCH_V5_LIMIT.events.OrderFilled().process_receipt(r_)
    v6_limit_events = ONEINCH_V6_LIMIT.events.OrderFilled().process_receipt(r_)
    transfers = token.events.Transfer().process_receipt(r_)
    first_log_index = r_['logs'][0]['logIndex']
    limit = []
    for event in v5_limit_events:
        index = event['logIndex']
        # Try skipping fusion swaps, can start with an approval
        if index == first_log_index or index == first_log_index + 1:
            continue
        # In v5 next two tokens transfers should be the swap
        next_two = [e for e in transfers if e['logIndex'] > index]
        assert len(next_two) >= 2
        in_, out_ = next_two[0], next_two[1]
        if not (in_['args']['from'] == out_['args']['to'] or in_['args']['to'] == out_['args']['from']):
            logger.warning('Unmatched 1inch v5 limit order')
            continue
        maker_token, maker_amount = in_['address'], in_['args']['value']
        taker_token, taker_amount = out_['address'], out_['args']['value']

        limit_action = {
            'pool_address': AGG_ROUTER_V5,
            'protocol': 'oneinch_v5_limit',
            'token_out': maker_token,
            'amount_out': maker_amount,
            'token_in': taker_token,
            'amount_in': taker_amount,
            'from': out_['args']['from'],
            'to': in_['args']['to'],
            'log_index': index
        }
        limit.append(limit_action)

    for event in v6_limit_events:
        index = event['logIndex']
        # Try skipping fusion swaps, can start with an approval
        if index == first_log_index or index == first_log_index + 1:
            continue
        # In v6 previous two tokens transfers should be the swap
        prev_two = [e for e in transfers if e['logIndex'] < index]
        if not len(prev_two) >= 2:
            logger.warning('Unmatched 1inch v6 limit order')
            continue
        in_, out_ = prev_two[-2], prev_two[-1]
        if not (in_['args']['from'] == out_['args']['to'] or in_['args']['to'] == out_['args']['from']):
            logger.warning('Unmatched 1inch v6 limit order')
            continue
        maker_token, maker_amount = in_['address'], in_['args']['value']
        taker_token, taker_amount = out_['address'], out_['args']['value']

        limit_action = {
            'pool_address': AGG_ROUTER_V6,
            'protocol': 'oneinch_v6_limit',
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
        assert (next_two[1]['args']['value'] == amount_in or next_two[1]['args']['from'] == event['args']['recipient'])
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
    token = w3.eth.contract(address=stETH, abi=STETH)
    transfers = token.events.Transfer().process_receipt(r_)

    steth_wraps = [t for t in transfers if
                   t.address == stETH and t['args'][
                       'to'] == wstETH]
    actions = []
    for wrap in steth_wraps:
        from_ = wrap['args']['from']
        index = wrap['logIndex']
        if from_ != ZERO:  # Not the chained WETH --> stETH --> wstETH case
            previous = [e for e in transfers if e['logIndex'] < wrap['logIndex']
                        and e['address'] == wstETH]
            assert len(previous) > 0
            wsteth_log = previous[-1]
            assert wsteth_log['args']['to'] == from_
        else:  # stETH gets sent from ZERO, means it just got minted and wstETH transfer will be AFTER
            next_ = [e for e in transfers if e['logIndex'] > wrap['logIndex']
                     and e['address'] == wstETH]
            assert len(next_) > 0
            wsteth_log = next_[0]
        wrap_action = {
            'pool_address': wstETH,
            'from': from_,
            'to': from_,
            'protocol': 'steth_wrap',
            'token_in': stETH,
            'amount_in': wrap['args']['value'],
            'token_out': wstETH,
            'amount_out': wsteth_log['args']['value'],
            'log_index': index
        }
        actions.append(wrap_action)

    steth_unwraps = [t for t in transfers if
                     t.address == stETH and t['args'][
                         'from'] == wstETH]

    for unwrap in steth_unwraps:
        to_ = unwrap['args']['to']
        index = unwrap['logIndex']
        previous = [e for e in transfers if e['logIndex'] < unwrap['logIndex']
                    and e['address'] == wstETH]
        assert len(previous) > 0
        wsteth_log = previous[-1]
        assert wsteth_log['args']['from'] == to_
        wrap_action = {
            'pool_address': wstETH,
            'from': to_,
            'to': to_,
            'protocol': 'steth_unwrap',
            'token_in': wstETH,
            'amount_in': wsteth_log['args']['value'],
            'token_out': stETH,
            'amount_out': unwrap['args']['value'],
            'log_index': index
        }
        actions.append(wrap_action)

    steth_mints = [t for t in transfers if
                   t.address == stETH and t['args'][
                       'from'] == ZERO]
    for mint in steth_mints:
        to_ = mint['args']['to']
        deposits = token.events.Submitted().process_receipt(r_)
        prev_deposits = [d for d in deposits if d['logIndex'] < mint['logIndex']]
        assert len(prev_deposits) > 0
        deposit_log = prev_deposits[-1]
        assert deposit_log['address'] == stETH
        assert deposit_log['args']['sender'] == to_
        mint_action = {
            'pool_address': stETH,
            'from': to_,
            'to': to_,
            'protocol': 'steth_mint',
            'token_in': WETH,
            'amount_in': deposit_log['args']['amount'],
            'token_out': stETH,
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
            logger.info(f"Missing token {from_address}")
        if to_address is None:
            logger.info(f"Missing token {to_address}")
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
    withdrawals = token.events.Withdraw().process_receipt(r_)
    withdrawals = [w for w in withdrawals if w['address'] == '0x83F20F44975D03b1b09e64809B757c47f942BEeA']
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

    for w in withdrawals:
        action = {
            'pool_address': '0x83F20F44975D03b1b09e64809B757c47f942BEeA',
            'protocol': 'sdai_burn',
            'token_in': '0x83F20F44975D03b1b09e64809B757c47f942BEeA',
            'amount_in': w['args']['shares'],
            'token_out': TOKENS['DAI'],
            'amount_out': w['args']['assets'],
            'from': w['args']['caller'],
            'to': w['args']['receiver'],
            'log_index': w['logIndex']
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
            tally['WETH'] -= d['amount_out']
        else:
            tally[d['token_out']] -= d['amount_out']
    return tally


def extract_swaps(r):
    swap_events = {
        'BALANCER_V1': BALANCER_V1.events.LOG_SWAP().process_receipt(r),
        'BALANCER_V2': BALANCER_V2.events.Swap().process_receipt(r),
        'DODO': DODO.events.SellBaseToken().process_receipt(r) + DODO.events.BuyBaseToken().process_receipt(r),
        'DODO_V2': DODO_V2.events.DODOSwap().process_receipt(r),
        'UNI_V1': UNI_V1.events.TokenPurchase().process_receipt(r) + UNI_V1.events.EthPurchase().process_receipt(r),
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
        'SDAI': get_sdai_actions(r),
        'SMOOTHY_V1': SMOOTHY_V1.events.Swap().process_receipt(r),
        'FIXED_RATE': FIXED_RATE.events.Swap().process_receipt(r),
        'SMARDEX': SMARDEX.events.Swap().process_receipt(r),
    }

    # aave_actions = get_aave_actions(r)
    # swap_events['AAVE_ACTIONS'] = get_aave_actions(r)
    return {k: v for k, v in swap_events.items() if v}


def main():
    # logger.info('Loading data')
    data = pd.read_csv('/home/robert/Projects/liquidity-parser/odos.csv')
    data = data.dropna()
    data = data.sort_values('amount_usd', ascending=False).reset_index(drop=True)
    data = data[
        ~((data['token_sold_symbol'].isin(['WETH', 'ETH'])) & (data['token_bought_symbol'].isin(['WETH', 'ETH'])))]
    # data = data[
    #     data['tx_to'].isin(['0x1111111254eeb25477b68fb85ed929f73a960582',
    #                         '0xad3b67bca8935cb510c8d18bd45f0b94f54a968f',
    # '0x111111125421ca6dc452d289314280a0f8842a65'])]
    logger.info('Data loaded')
    # cache = load_pool_cache()
    # Weird metapool events: https://etherscan.io/tx/0x48a571b2e7a842a0c0a1981433de9e7e582bf6ad3f6adc217439afcca451c178
    # receipt = w3.eth.get_transaction_receipt('0xa2ba7939818d920aef9d1b2e1222d4df962ac30610367c0ec67c3a0fb3c5dbbc') Cowswap DAO
    # receipt = w3.eth.get_transaction_receipt('0xb9aa4a0e4739857b0be9844863a2d7375d6889fd247acf616b6431dda1b9704b')
    # receipt = w3.eth.get_transaction_receipt('0x8ff9cb9838d46c1df4c897274a5066df67c766a5370bfc4cee6a8c9ecc7f541f')
    # receipt = w3.eth.get_transaction_receipt('0x746abc3b9a30dd4ef17bc6033d53a88243b6438857c73a353102eeefbef1e7c6')
    # receipt = w3.eth.get_transaction_receipt('0x69eb97caa4293d771f1e6cfb2c1dd98bd513369f9d772fef78178741b448a374')
    # receipt = w3.eth.get_transaction_receipt('0x333fd06a7079a6420b8f125c7043d9667b47fcd85db6f83fe3a105a918a9f570')
    # transfers = extract_erc20_transfers(receipt)
    # swaps = extract_swaps(receipt)
    # dag = generate_swap_dag(swaps, transfers, symbols=True)
    # logger.info(f"Protocols used:{list(swaps.keys())}")
    # pprint(dag)
    # pprint(dict(tally_dag(dag)))
    # import ipdb;
    # ipdb.set_trace()

    # with open('parsed.json') as f:
    #     parsed = json.load(f)
    for i, r in data.reset_index(drop=True).iterrows():
        if i < 783:
            continue
        tx_hash = r['tx_hash']
        logger.info(f"Processing transaction {i}: {tx_hash}")
        # logger.info(f"Num trades {r['num_trades']}, volume {int(r['batch_value'])} USD, solver {r['solver']}")
        receipt = w3.eth.get_transaction_receipt(r['tx_hash'])
        swaps = extract_swaps(receipt)
        transfers = extract_erc20_transfers(receipt)
        dag = generate_swap_dag(swaps, transfers, symbols=True)
        logger.info(f"Protocols used:{swaps.keys()}")
        # parsed[r['tx_hash']] = dag
        # if i % 50 == 0:
        #     with open('parsed.json', 'w') as f:
        #         json.dump(parsed, f, indent=2)
        pprint(dict(tally_dag(dag)))
    import ipdb;
    ipdb.set_trace()


if __name__ == '__main__':
    # logging.basicConfig(encoding='utf-8', level=logging.INFO)
    main()
