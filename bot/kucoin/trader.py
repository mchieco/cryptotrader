from decimal import Decimal
import time
from kucoin.client import Market, Trade
from dca_portfolio import Coin
import os
from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp

def run_trades(coin_list: list[Coin]):
    with ThreadPoolExecutor(max_workers=mp.cpu_count()) as pool:
        pool.map(run, coin_list)

def run(coin: Coin):
    public_client = Market()
    private_client = Trade(
        key=os.getenv("kucoin_api_key"),
        secret=os.getenv("kucoin_api_secret"),
        passphrase=os.getenv("kucoin_api_passphrase"),
    )
    ticker = coin.ticker
    amount = coin.buy_amount
    precision_value = _get_precision_value(public_client, ticker)
    if ticker.split("-")[1] == ("USDT" or "USDC"):
        bid_price = Decimal(public_client.get_ticker(ticker)["bestBid"])
        amount_to_buy = amount / bid_price
        order_id = private_client.create_limit_order(
            ticker,
            "buy",
            str(f"{amount_to_buy:.{precision_value}f}"),
            str(bid_price),
        )["orderId"]
        order = private_client.get_order_details(order_id)
        print(
            f'Order placed for {order["size"]} amount of {ticker} for {order["price"]}'
        )
        is_live = order["isActive"]
        new_buy_counter = 6
        while is_live:
            order = private_client.get_order_details(order["id"])
            is_live = order["isActive"]
            print(f"Checking order status, is filled?: {not is_live}")
            if new_buy_counter < 1:
                private_client.cancel_order(order["id"])
                print(f"canceled order with id {order['id']}")
                bid_price = Decimal(public_client.get_ticker(ticker)["bestBid"])
                order_id = private_client.create_limit_order(
                    ticker,
                    "buy",
                    str(f"{amount_to_buy:.{precision_value}f}"),
                    str(bid_price),
                )["orderId"]
                order = private_client.get_order_details(order_id)
                print(
                    f'New order placed for {order["size"]} amount of {ticker} for {order["price"]}'
                )
                new_buy_counter = 6
            time.sleep(10)
            new_buy_counter -= 1
    else:
        crypto_to_crypto_bid_price = public_client.get_ticker(ticker)["bestBid"]
        usd_price = public_client.get_ticker(f"{ticker.split('-')[1]}-USDT")[
            "price"
        ]
        price_in_usd = Decimal(crypto_to_crypto_bid_price) * Decimal(usd_price)
        amount_to_buy = amount / price_in_usd
        order_id = private_client.create_limit_order(
            ticker,
            "buy",
            str(f"{amount_to_buy:.{precision_value}f}"),
            crypto_to_crypto_bid_price,
        )["orderId"]
        order = private_client.get_order_details(order_id)
        print(
            f'Order placed for {order["size"]} amount of {ticker} for {order["price"]}'
        )
        is_live = order["isActive"]
        new_buy_counter = 6
        while is_live:
            time.sleep(10)
            order = private_client.get_order_details(order["id"])
            is_live = order["isActive"]
            print(f"Checking order status, is filled?: {not is_live}")
            if new_buy_counter < 1:
                private_client.cancel_order(order["id"])
                print(f"canceled order with id {order['id']}")
                crypto_to_crypto_bid_price = public_client.get_ticker(ticker)[
                    "bestBid"
                ]
                usd_price = public_client.get_ticker(
                    f"{ticker.split('-')[1]}-USDT"
                )["price"]
                price_in_usd = Decimal(crypto_to_crypto_bid_price) * Decimal(
                    usd_price
                )
                amount_to_buy = amount / price_in_usd
                order_id = private_client.create_limit_order(
                    ticker,
                    "buy",
                    str(f"{amount_to_buy:.{precision_value}f}"),
                    crypto_to_crypto_bid_price,
                )["orderId"]
                order = private_client.get_order_details(order_id)
                print(
                    f'New order placed for {order["size"]} amount of {ticker} for {order["price"]}'
                )
                new_buy_counter = 6
            new_buy_counter -= 1

    print(f'Bought {order["size"]} amount of {ticker} for {order["price"]}')


def _get_precision_value(public_client: Market, symbol: str) -> int:
    tick_size = _get_symbol_details(public_client, symbol)["baseIncrement"]
    return len(tick_size.split(".")[1])


def _get_symbol_details(public_client: Market, symbol: str):
    symbol_list = public_client.get_symbol_list()
    for symbol_item in symbol_list:
        if symbol_item["symbol"] == symbol:
            return symbol_item
    raise Exception("could not find symbol in list for currency")


def sell_order(ticker: str, amount: str, price: str):
    public_client = Market()
    private_client = Trade(
        key=os.getenv("kucoin_api_key"),
        secret=os.getenv("kucoin_api_secret"),
        passphrase=os.getenv("kucoin_api_passphrase"),
    )
    if not price:
        price = public_client.get_ticker(ticker)["bestAsk"]
    order_id = private_client.create_limit_order(ticker, "sell", amount, price)[
        "orderId"
    ]
    order = private_client.get_order_details(order_id)
    print(f'Sold {order["size"]} amount of {ticker} for {order["price"]}')
