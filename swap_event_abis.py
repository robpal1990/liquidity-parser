DODO = [{
    "anonymous": False,
    "inputs": [
        {
            "indexed": True,
            "internalType": "address",
            "name": "seller",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "payBase",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "receiveQuote",
            "type": "uint256"}],
    "name": "SellBaseToken",
    "type": "event"},
    {
        "anonymous": False,
        "inputs": [{
            "indexed": True,
            "internalType": "address",
            "name": "buyer",
            "type": "address"},
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "receiveBase",
                "type": "uint256"},
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "payQuote",
                "type": "uint256"}],
        "name": "BuyBaseToken",
        "type": "event"}
]

DODO_V2 = [{
    "anonymous": False,
    "inputs": [
        {
            "indexed": False,
            "internalType": "address",
            "name": "fromToken",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "address",
            "name": "toToken",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "fromAmount",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "toAmount",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "address",
            "name": "trader",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "address",
            "name": "receiver",
            "type": "address"}],
    "name": "DODOSwap",
    "type": "event"}]

BALANCER_V1 = [{
    "anonymous": False,
    "inputs": [
        {
            "indexed": True,
            "internalType": "address",
            "name": "caller",
            "type": "address"},
        {
            "indexed": True,
            "internalType": "address",
            "name": "tokenIn",
            "type": "address"},
        {
            "indexed": True,
            "internalType": "address",
            "name": "tokenOut",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "tokenAmountIn",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "tokenAmountOut",
            "type": "uint256"}],
    "name": "LOG_SWAP",
    "type": "event"}]

# BALANCER_V2, SWAAP_V2
BALANCER_V2 = [{
    "anonymous": False,
    "inputs": [{
        "indexed": True,
        "internalType": "bytes32",
        "name": "poolId",
        "type": "bytes32"},
        {
            "indexed": True,
            "internalType": "contract IERC20",
            "name": "tokenIn",
            "type": "address"},
        {
            "indexed": True,
            "internalType": "contract IERC20",
            "name": "tokenOut",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "amountIn",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "amountOut",
            "type": "uint256"}],
    "name": "Swap",
    "type": "event"}]

C = [{
    "name": "TokenExchange",
    "inputs": [
        {
            "name": "buyer",
            "type": "address",
            "indexed": True},
        {
            "name": "sold_id",
            "type": "uint256",
            "indexed": False}, {
            "name": "tokens_sold",
            "type": "uint256",
            "indexed": False}, {
            "name": "bought_id",
            "type": "uint256",
            "indexed": False}, {
            "name": "tokens_bought",
            "type": "uint256",
            "indexed": False}],
    "anonymous": False,
    "type": "event"}]

CURVE_V1 = [{
    "name": "TokenExchange",
    "inputs": [
        {
            "type": "address",
            "name": "buyer",
            "indexed": True},
        {
            "type": "int128",
            "name": "sold_id",
            "indexed": False},
        {
            "type": "uint256",
            "name": "tokens_sold",
            "indexed": False},
        {
            "type": "int128",
            "name": "bought_id",
            "indexed": False},
        {
            "type": "uint256",
            "name": "tokens_bought",
            "indexed": False}],
    "anonymous": False,
    "type": "event"},
    {
        "name": "TokenExchangeUnderlying",
        "inputs": [{
            "type": "address",
            "name": "buyer",
            "indexed": True},
            {
                "type": "int128",
                "name": "sold_id",
                "indexed": False},
            {
                "type": "uint256",
                "name": "tokens_sold",
                "indexed": False},
            {
                "type": "int128",
                "name": "bought_id",
                "indexed": False},
            {
                "type": "uint256",
                "name": "tokens_bought",
                "indexed": False}],
        "anonymous": False,
        "type": "event"}]

CURVE_V2 = [
    {
        "name": "TokenExchange",
        "inputs": [
            {
                "name": "buyer",
                "type": "address",
                "indexed": True},
            {
                "name": "sold_id",
                "type": "uint256",
                "indexed": False},
            {
                "name": "tokens_sold",
                "type": "uint256",
                "indexed": False},
            {
                "name": "bought_id",
                "type": "uint256",
                "indexed": False},
            {
                "name": "tokens_bought",
                "type": "uint256",
                "indexed": False},
            {
                "name": "fee",
                "type": "uint256",
                "indexed": False},
            {
                "name": "packed_price_scale",
                "type": "uint256",
                "indexed": False}],
        "anonymous": False,
        "type": "event"}]

CURVE_V2_1 = [
    {
        "name": "TokenExchange",
        "inputs": [
            {
                "name": "buyer",
                "type": "address",
                "indexed": True},
            {
                "name": "sold_id",
                "type": "uint256",
                "indexed": False},
            {
                "name": "tokens_sold",
                "type": "uint256",
                "indexed": False},
            {
                "name": "bought_id",
                "type": "uint256",
                "indexed": False},
            {
                "name": "tokens_bought",
                "type": "uint256",
                "indexed": False}],
        "anonymous": False,
        "type": "event"}]

# UNI_V2, SUSHI, SHIBA, CRO
UNI_V2 = [{
    "name": "Swap",
    "inputs": [
        {
            "indexed": True,
            "internalType": "address",
            "name": "sender",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "amount0In",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "amount1In",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "amount0Out",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "amount1Out",
            "type": "uint256"},
        {
            "indexed": True,
            "internalType": "address",
            "name": "to",
            "type": "address"}],
    "anonymous": False,
    "type": "event"}]

# UNI_V3, KYBER_ELASTIC, SOLIDLY_V3
UNI_V3 = [{
    "anonymous": False,
    "inputs": [
        {
            "indexed": True,
            "internalType": "address",
            "name": "sender",
            "type": "address"},
        {
            "indexed": True,
            "internalType": "address",
            "name": "recipient",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "int256",
            "name": "amount0",
            "type": "int256"},
        {
            "indexed": False,
            "internalType": "int256",
            "name": "amount1",
            "type": "int256"},
        {
            "indexed": False,
            "internalType": "uint160",
            "name": "sqrtPriceX96",
            "type": "uint160"},
        {
            "indexed": False,
            "internalType": "uint128",
            "name": "liquidity",
            "type": "uint128"},
        {
            "indexed": False,
            "internalType": "int24",
            "name": "tick",
            "type": "int24"}],
    "name": "Swap",
    "type": "event"}]

PANCAKE_V3 = [{
    "anonymous": False,
    "inputs": [
        {
            "indexed": True,
            "internalType": "address",
            "name": "sender",
            "type": "address"},
        {
            "indexed": True,
            "internalType": "address",
            "name": "recipient",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "int256",
            "name": "amount0",
            "type": "int256"},
        {
            "indexed": False,
            "internalType": "int256",
            "name": "amount1",
            "type": "int256"},
        {
            "indexed": False,
            "internalType": "uint160",
            "name": "sqrtPriceX96",
            "type": "uint160"},
        {
            "indexed": False,
            "internalType": "uint128",
            "name": "liquidity",
            "type": "uint128"},
        {
            "indexed": False,
            "internalType": "int24",
            "name": "tick",
            "type": "int24"},
        {
            "indexed": False,
            "internalType": "uint128",
            "name": "protocolFeesToken0",
            "type": "uint128"},
        {
            "indexed": False,
            "internalType": "uint128",
            "name": "protocolFeesToken1",
            "type": "uint128"}],
    "name": "Swap",
    "type": "event"}]

UNI = [{
    "name": "TokenPurchase",
    "inputs": [
        {
            "type": "address",
            "name": "buyer",
            "indexed": True},
        {
            "type": "uint256",
            "name": "eth_sold",
            "indexed": True},
        {
            "type": "uint256",
            "name": "tokens_bought",
            "indexed": True}],
    "anonymous": False,
    "type": "event"},
    {
        "name": "EthPurchase",
        "inputs": [
            {
                "type": "address",
                "name": "buyer",
                "indexed": True},
            {
                "type": "uint256",
                "name": "tokens_sold",
                "indexed": True},
            {
                "type": "uint256",
                "name": "eth_bought",
                "indexed": True}],
        "anonymous": False,
        "type": "event"}]

MAV_V1 = [{
    "anonymous": False,
    "inputs": [
        {
            "indexed": False,
            "internalType": "address",
            "name": "sender",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "address",
            "name": "recipient",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "bool",
            "name": "tokenAIn",
            "type": "bool"},
        {
            "indexed": False,
            "internalType": "bool",
            "name": "exactOutput",
            "type": "bool"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "amountIn",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "amountOut",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "int32",
            "name": "activeTick",
            "type": "int32"}],
    "name": "Swap",
    "type": "event"}]

BANCOR_V3 = [{
    "anonymous": False,
    "inputs": [
        {
            "indexed": True,
            "internalType": "bytes32",
            "name": "contextId",
            "type": "bytes32"},
        {
            "indexed": True,
            "internalType": "contract Token",
            "name": "sourceToken",
            "type": "address"},
        {
            "indexed": True,
            "internalType": "contract Token",
            "name": "targetToken",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "sourceAmount",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "targetAmount",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "bntAmount",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "targetFeeAmount",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "bntFeeAmount",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "address",
            "name": "trader",
            "type": "address"}],
    "name": "TokensTraded",
    "type": "event"}]

# PSM = {
#            "anonymous": True,
#            "inputs": [{
#                           "indexed": True,
#                           "internalType": "bytes4",
#                           "name": "sig",
#                           "type": "bytes4"}, {
#                           "indexed": True,
#                           "internalType": "address",
#                           "name": "usr",
#                           "type": "address"}, {
#                           "indexed": True,
#                           "internalType": "bytes32",
#                           "name": "arg1",
#                           "type": "bytes32"}, {
#                           "indexed": True,
#                           "internalType": "bytes32",
#                           "name": "arg2",
#                           "type": "bytes32"}, {
#                           "indexed": False,
#                           "internalType": "bytes",
#                           "name": "data",
#                           "type": "bytes"}],
#            "name": "LogNote",
#            "type": "event"}

# Needs tokens from contract call token0/token1
KYBER = [{
    "anonymous": False,
    "inputs": [
        {
            "indexed": True,
            "internalType": "address",
            "name": "sender",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "amount0In",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "amount1In",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "amount0Out",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "amount1Out",
            "type": "uint256"},
        {
            "indexed": True,
            "internalType": "address",
            "name": "to",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "feeInPrecision",
            "type": "uint256"}],
    "name": "Swap",
    "type": "event"}]

# call getToken for id<>address mapping
SYNAPSE = [{
    "anonymous": False,
    "inputs": [
        {
            "indexed": True,
            "internalType": "address",
            "name": "buyer",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "tokensSold",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "tokensBought",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint128",
            "name": "soldId",
            "type": "uint128"},
        {
            "indexed": False,
            "internalType": "uint128",
            "name": "boughtId",
            "type": "uint128"}],
    "name": "TokenSwap",
    "type": "event"}]

CLIPPER = [{
    "anonymous": False,
    "inputs": [
        {
            "indexed": True,
            "internalType": "address",
            "name": "inAsset",
            "type": "address"},
        {
            "indexed": True,
            "internalType": "address",
            "name": "outAsset",
            "type": "address"},
        {
            "indexed": True,
            "internalType": "address",
            "name": "recipient",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "inAmount",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "outAmount",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "bytes",
            "name": "auxiliaryData",
            "type": "bytes"}],
    "name": "Swapped",
    "type": "event"}]

OTC_ORDER = [{
    "anonymous": False,
    "inputs": [
        {
            "indexed": False,
            "internalType": "bytes32",
            "name": "orderHash",
            "type": "bytes32"},
        {
            "indexed": False,
            "internalType": "address",
            "name": "maker",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "address",
            "name": "taker",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "address",
            "name": "makerToken",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "address",
            "name": "takerToken",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "uint128",
            "name": "makerTokenFilledAmount",
            "type": "uint128"},
        {
            "indexed": False,
            "internalType": "uint128",
            "name": "takerTokenFilledAmount",
            "type": "uint128"}],
    "name": "OtcOrderFilled",
    "type": "event"}]

HASHFLOW = [{
    "anonymous": False,
    "inputs": [
        {
            "indexed": False,
            "internalType": "address",
            "name": "trader",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "address",
            "name": "effectiveTrader",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "bytes32",
            "name": "txid",
            "type": "bytes32"},
        {
            "indexed": False,
            "internalType": "address",
            "name": "baseToken",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "address",
            "name": "quoteToken",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "baseTokenAmount",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "quoteTokenAmount",
            "type": "uint256"}],
    "name": "Trade",
    "type": "event"}]

RFQ_ORDER = [
    # {
    #     "anonymous": False,
    #     "inputs": [
    #         {
    #             "indexed": False,
    #             "internalType": "bytes32",
    #             "name": "orderHash",
    #             "type": "bytes32"},
    #         {
    #             "indexed": False,
    #             "internalType": "address",
    #             "name": "maker",
    #             "type": "address"},
    #         {
    #             "indexed": False,
    #             "internalType": "address",
    #             "name": "taker",
    #             "type": "address"},
    #         {
    #             "indexed": False,
    #             "internalType": "address",
    #             "name": "feeRecipient",
    #             "type": "address"},
    #         {
    #             "indexed": False,
    #             "internalType": "address",
    #             "name": "makerToken",
    #             "type": "address"},
    #         {
    #             "indexed": False,
    #             "internalType": "address",
    #             "name": "takerToken",
    #             "type": "address"},
    #         {
    #             "indexed": False,
    #             "internalType": "uint128",
    #             "name": "takerTokenFilledAmount",
    #             "type": "uint128"},
    #         {
    #             "indexed": False,
    #             "internalType": "uint128",
    #             "name": "makerTokenFilledAmount",
    #             "type": "uint128"},
    #         {
    #             "indexed": False,
    #             "internalType": "uint128",
    #             "name": "takerTokenFeeFilledAmount",
    #             "type": "uint128"},
    #         {
    #             "indexed": False,
    #             "internalType": "uint256",
    #             "name": "protocolFeePaid",
    #             "type": "uint256"},
    #         {
    #             "indexed": False,
    #             "internalType": "bytes32",
    #             "name": "pool",
    #             "type": "bytes32"}],
    #     "name": "LimitOrderFilled",
    #     "type": "event"},
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "orderHash",
                "type": "bytes32"},
            {
                "indexed": False,
                "internalType": "address",
                "name": "maker",
                "type": "address"},
            {
                "indexed": False,
                "internalType": "address",
                "name": "taker",
                "type": "address"},
            {
                "indexed": False,
                "internalType": "address",
                "name": "makerToken",
                "type": "address"},
            {
                "indexed": False,
                "internalType": "address",
                "name": "takerToken",
                "type": "address"},
            {
                "indexed": False,
                "internalType": "uint128",
                "name": "takerTokenFilledAmount",
                "type": "uint128"},
            {
                "indexed": False,
                "internalType": "uint128",
                "name": "makerTokenFilledAmount",
                "type": "uint128"},
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "pool",
                "type": "bytes32"}],
        "name": "RfqOrderFilled",
        "type": "event"}]

ONEINCH_RFQ = [{
    "anonymous": False,
    "inputs": [
        {
            "indexed": True,
            "internalType": "address",
            "name": "maker",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "bytes32",
            "name": "orderHash",
            "type": "bytes32"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "remaining",
            "type": "uint256"}],
    "name": "OrderFilled",
    "type": "event"}, {
    "anonymous": False,
    "inputs": [
        {
            "indexed": False,
            "internalType": "bytes32",
            "name": "orderHash",
            "type": "bytes32"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "makingAmount",
            "type": "uint256"}],
    "name": "OrderFilledRFQ",
    "type": "event"}]

INTEGRAL = [{
    "anonymous": False,
    "inputs": [
        {
            "indexed": True,
            "internalType": "address",
            "name": "sender",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "address",
            "name": "tokenIn",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "address",
            "name": "tokenOut",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "amountIn",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "amountInMax",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "amountOut",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "bool",
            "name": "wrapUnwrap",
            "type": "bool"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "fee",
            "type": "uint256"},
        {
            "indexed": True,
            "internalType": "address",
            "name": "to",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "address",
            "name": "orderContract",
            "type": "address"},
        {
            "indexed": True,
            "internalType": "uint256",
            "name": "orderId",
            "type": "uint256"}],
    "name": "Buy",
    "type": "event"},
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "sender",
                "type": "address"},
            {
                "indexed": False,
                "internalType": "address",
                "name": "tokenIn",
                "type": "address"},
            {
                "indexed": False,
                "internalType": "address",
                "name": "tokenOut",
                "type": "address"},
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amountIn",
                "type": "uint256"},
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amountOut",
                "type": "uint256"},
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amountOutMin",
                "type": "uint256"},
            {
                "indexed": False,
                "internalType": "bool",
                "name": "wrapUnwrap",
                "type": "bool"},
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "fee",
                "type": "uint256"},
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address"},
            {
                "indexed": False,
                "internalType": "address",
                "name": "orderContract",
                "type": "address"},
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "orderId",
                "type": "uint256"}],
        "name": "Sell",
        "type": "event"}]

SNX = [{
    "anonymous": False,
    "inputs": [
        {
            "indexed": True,
            "internalType": "address",
            "name": "account",
            "type": "address"},
        {
            "indexed": False,
            "internalType": "bytes32",
            "name": "fromCurrencyKey",
            "type": "bytes32"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "fromAmount",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "bytes32",
            "name": "toCurrencyKey",
            "type": "bytes32"},
        {
            "indexed": False,
            "internalType": "uint256",
            "name": "toAmount",
            "type": "uint256"},
        {
            "indexed": False,
            "internalType": "address",
            "name": "toAddress",
            "type": "address"}],
    "name": "AtomicSynthExchange",
    "type": "event"}]

BEBOP_RFQ = [
    {"anonymous": False,
     "inputs": [
         {"indexed": False,
          "internalType": "bytes32",
          "name": "order_hash",
          "type": "bytes32"}],
     "name": "AggregateOrderExecuted",
     "type": "event"}]
