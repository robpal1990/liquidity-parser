import json
import logging
import warnings
from pprint import pprint

from web3 import Web3

from abis import AAVE_LENDING_V2
from addresses import TOKENS, ZERO, PSM_USDC_A, MCD_PSM_USDC_A
from swap_event_abis import BALANCER_V1, BALANCER_V2, UNI, UNI_V2, UNI_V3, CURVE_V1, CURVE_V2, CURVE_V2_1, PANCAKE_V3, \
    SYNAPSE, BANCOR_V3, KYBER, MAV_V1, DODO, DODO_V2, CLIPPER, OTC_ORDER, RFQ_ORDER, HASHFLOW, ONEINCH_RFQ, INTEGRAL, \
    SNX, BEBOP_RFQ
from token_abis import STETH, AAVE_TOKEN, ERC20
from utils import generate_swap_dag

warnings.filterwarnings("ignore")

logging.getLogger("web3").setLevel(logging.CRITICAL)

RPC_URL = 'http://localhost:8545'
w3 = Web3(Web3.HTTPProvider(RPC_URL))

BALANCER_V1 = w3.eth.contract(address=None, abi=BALANCER_V1)
BALANCER_V2 = w3.eth.contract(address=None, abi=BALANCER_V2)  # Also SWAAP_V2
DODO = w3.eth.contract(address=None, abi=DODO)
DODO_V2 = w3.eth.contract(address=None, abi=DODO_V2)
UNI = w3.eth.contract(address=None, abi=UNI)
UNI_V2 = w3.eth.contract(address=None, abi=UNI_V2)  # Also: SUSHI, SHIBA, CRO, INTEGRAL, NOMISWAP, PANCAKE, FRAXSWAP
UNI_V3 = w3.eth.contract(address=None, abi=UNI_V3)  # Also: KYBER_ELASTIC, SOLIDLY_V3
PANCAKE_V3 = w3.eth.contract(address=None, abi=PANCAKE_V3)
CURVE_V1 = w3.eth.contract(address=None, abi=CURVE_V1)
CURVE_V2 = w3.eth.contract(address=None, abi=CURVE_V2)
CURVE_V2_1 = w3.eth.contract(address=None, abi=CURVE_V2_1)
SYNAPSE = w3.eth.contract(address=None, abi=SYNAPSE)
BANCOR_V3 = w3.eth.contract(address=None, abi=BANCOR_V3)
KYBER = w3.eth.contract(address=None, abi=KYBER)
MAV_V1 = w3.eth.contract(address=None, abi=MAV_V1)
CLIPPER = w3.eth.contract(address=None, abi=CLIPPER)
OTC_ORDER = w3.eth.contract(address=None, abi=OTC_ORDER)
HASHFLOW = w3.eth.contract(address=None, abi=HASHFLOW)
RFQ_ORDER = w3.eth.contract(address=None, abi=RFQ_ORDER)
ONEINCH_RFQ = w3.eth.contract(address=None, abi=ONEINCH_RFQ)
BEBOP_RFQ = w3.eth.contract(address=None, abi=BEBOP_RFQ)
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
    # limit_events = ONEINCH_RFQ.events.OrderFilled().process_receipt(r_)
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


def get_steth_actions(r):
    """
    web3py AttrDicts are annoying, because one cannot dot-access `from` and
    `to` parameters as these are Python keywords. Therefore we parse them
    as normal dicts.
    """
    first_log_index = r['logs'][0]['logIndex']
    token = w3.eth.contract(address=TOKENS['stETH'], abi=STETH)
    transfers = token.events.Transfer().process_receipt(r)

    steth_wraps = [t for t in transfers if
                   t.address == TOKENS['stETH'] and t['args'][
                       'to'] == TOKENS['wstETH']]
    wraps = []
    for wrap in steth_wraps:
        from_ = wrap['args']['from']
        index = wrap['logIndex']
        wsteth_log = token.events.Transfer().process_log(r['logs'][index - 1 - first_log_index])
        assert wsteth_log['address'] == TOKENS['wstETH']
        assert wsteth_log['args']['to'] == from_
        wrap_action = {
            'address': from_,
            'stETH_out': wrap['args']['value'],
            'wstETH_in': wsteth_log['args']['value'],
            'log_index': index
        }
        wraps.append(wrap_action)

    steth_unwraps = [t for t in transfers if
                     t.address == TOKENS['stETH'] and t['args'][
                         'from'] == TOKENS['wstETH']]
    unwraps = []
    for unwrap in steth_unwraps:
        to_ = unwrap['args']['to']
        index = unwrap['logIndex']
        wsteth_log = token.events.Transfer().process_log(r['logs'][index - 1 - first_log_index])
        assert wsteth_log['address'] == TOKENS['wstETH']
        assert wsteth_log['args']['from'] == to_
        wrap_action = {
            'address': to_,
            'stETH_in': unwrap['args']['value'],
            'wstETH_out': wsteth_log['args']['value'],
            'log_index': index
        }
        unwraps.append(wrap_action)

    steth_mints = [t for t in transfers if
                   t.address == TOKENS['stETH'] and t['args'][
                       'from'] == ZERO]
    mints = []
    for mint in steth_mints:
        to_ = mint['args']['to']
        index = mint['logIndex']
        deposit_log = token.events.Submitted().process_log(r['logs'][index - 1 - first_log_index])
        assert deposit_log['address'] == TOKENS['stETH']
        assert deposit_log['args']['sender'] == to_
        mint_action = {
            'address': mint['args']['to'],
            'eth_in': deposit_log['args']['amount'],
            'stETH_out': mint['args']['value'],
            'log_index': index
        }
        mints.append(mint_action)

    return {
        'wraps': wraps,
        'unwraps': unwraps,
        'mints': mints
    }


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
            'address': s_['address'],
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
        dai_mints = [t for t in transfers if t['logIndex'] > u['logIndex']
                     and t['args']['from'] == ZERO and t['args']['to'] == u['args']['from']]

        assert len(dai_mints) > 0
        next_mint = dai_mints[0]
        swap = {
            'address': PSM_USDC_A,
            'protocol': 'psm_usdc_dai',
            'token_in': TOKENS['USDC'],
            'amount_in': u['args']['value'],
            'token_out': TOKENS['DAI'],
            'amount_out': next_mint['args']['value'],
            'from': u['args']['from'],
            'to': u['args']['from'],
            'log_index': u['logIndex']
        }
        swaps.append(swap)

    usdc_from_psm = [t for t in transfers if t['address'] == TOKENS['USDC']
                     and t['args']['from'] == PSM_USDC_A]
    for u in usdc_from_psm:
        dai_burns = [t for t in transfers if t['logIndex'] < u['logIndex']
                     and t['args']['from'] == u['args']['to'] and t['args']['to'] == MCD_PSM_USDC_A]

        assert len(dai_burns) > 0
        prev_burn = dai_burns[-1]
        swap = {
            'address': PSM_USDC_A,
            'protocol': 'psm_usdc_dai',
            'token_in': TOKENS['DAI'],
            'amount_in': prev_burn['args']['value'],
            'token_out': TOKENS['USDC'],
            'amount_out': u['args']['value'],
            'from': u['args']['to'],
            'to': u['args']['to'],
            'log_index': u['logIndex']
        }
        swaps.append(swap)

    return swaps


def get_frxeth_actions(r_):
    pass


def get_reth_actions(r_):
    # 0x649c9062ab55a490596a34a1c78783ed252f7ea06be5577e94fed14dab9fed89
    pass


def get_mkusd_actions(r_):
    # 0x1b75c69fb1e599ce4067b772d79bf926a98f4f2e409c83817a53567b2bdbb9c1
    pass


def get_sdai_actions(r_):
    # 0x0c067dc4d141e2476eed2653d99c840e9537daac3363dc94eb2d489719658f24
    pass


def extract_erc20_transfers(receipt):
    erc20 = w3.eth.contract(address=None, abi=ERC20)
    transfers = erc20.events.Transfer().process_receipt(receipt)
    return transfers


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
        'KYBER': KYBER.events.Swap().process_receipt(r),
        'MAV_V1': MAV_V1.events.Swap().process_receipt(r),
        'CLIPPER': CLIPPER.events.Swapped().process_receipt(r),
        'OTC_ORDER': OTC_ORDER.events.OtcOrderFilled().process_receipt(r),
        'HASHFLOW': HASHFLOW.events.Trade().process_receipt(r),
        'RFQ_ORDER': RFQ_ORDER.events.RfqOrderFilled().process_receipt(r),
        'INTEGRAL': INTEGRAL.events.Sell().process_receipt(r) + INTEGRAL.events.Buy().process_receipt(r),
        'SNX': get_snx_actions(r)
    }

    # stETH_actions = get_steth_actions(r)
    # aave_actions = get_aave_actions(r)
    # swap_events['STETH_ACTIONS'] = stETH_actions
    # swap_events['AAVE_ACTIONS'] = aave_actions
    swap_events['ONEINCH_RFQ'] = get_oneinch_rfq(r)
    swap_events['BEBOP_RFQ'] = get_bebop_rfq(r)
    swap_events['PSM_USDC'] = get_psm_usdc_actions(r)

    return {k: v for k, v in swap_events.items() if v}


def main():
    # logging.info('Loading data')
    # cowswap = pd.read_csv('/home/robert/Projects/crypto/one_inch_decoder/swaps.csv')
    # logging.info('Data loaded')
    cache = load_pool_cache()
    pools_cached = set([k for v in cache.values() for k in v.keys()])

    # Weird metapool events: https://etherscan.io/tx/0x48a571b2e7a842a0c0a1981433de9e7e582bf6ad3f6adc217439afcca451c178
    # receipt = w3.eth.get_transaction_receipt('0xe47c6496f1aa11dfd2205fffc91d48b52f6a952aab1ead585d3ca53826e8081f')
    # receipt = w3.eth.get_transaction_receipt('0x2ea334ce14efe486c8dc811f2ba9463812b95270963ed681e86957383d9651c9')
    # receipt = w3.eth.get_transaction_receipt('0xa2ba7939818d920aef9d1b2e1222d4df962ac30610367c0ec67c3a0fb3c5dbbc') Cowswap DAO
    receipt = w3.eth.get_transaction_receipt('0xdc1fab272e1b3393a929857a168b52a876e245d2a3d7da08c98e8e01c1274572')
    transfers = extract_erc20_transfers(receipt)
    swaps = extract_swaps(receipt)
    dag = generate_swap_dag(swaps, transfers)
    pprint(swaps.keys())

    import ipdb;
    ipdb.set_trace()

    for i, r in cowswap.iterrows():
        if i < 300:
            continue
        tx_hash = r['tx_hash']
        logging.info(f"Processing transaction {i}: {tx_hash}")
        swaps = extract_swaps(tx_hash)
        pools_involved = set([p['address'] for v in swaps.values() for p in v])
        # logging.info(f"Pools used:{pools_involved}")
        logging.info(f"New pools:{pools_involved - pools_cached}")

    import ipdb;
    ipdb.set_trace()


if __name__ == '__main__':
    logging.basicConfig(encoding='utf-8', level=logging.INFO)
    main()
