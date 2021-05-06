from decimal import Decimal
import time
from kucoin.client import Market, Trade
from dca_portfolio import Coin
import config


def run_trades(coin_list: list[Coin]):
    public_client = Market()
    for coin in coin_list:
        private_client = Trade(
            key=config.kucoin_api_key,
            secret=config.kucoin_api_secret,
            passphrase=config.kucoin_api_passphrase,
        )
        ticker = coin.ticker
        amount = coin.buy_amount
        if ticker.split("-")[1] == ("USDT" or "USDC"):
            bid_price = Decimal(public_client.get_ticker(ticker)["bestBid"])
            amount_to_buy = amount / bid_price
            order = private_client.create_limit_order(
                ticker, "buy", str(f"{amount_to_buy:.5f}"), str(bid_price)
            )
            is_live = order["isActive"]
            new_buy_counter = 6
            while is_live:
                order = private_client.get_order_details(order["orderId"])
                is_live = order["isActive"]
                if new_buy_counter < 1:
                    private_client.cancel_order(order["orderId"])
                    print(f"canceled order with id {order['id']}")
                    bid_price = Decimal(public_client.get_ticker(ticker)["bestBid"])
                    order = private_client.create_limit_order(
                        ticker, "buy", str(f"{amount_to_buy:.5f}"), str(bid_price)
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
            amount_to_buy = f"{Decimal(10) / price_in_usd:.5f}"
            order_id = private_client.create_limit_order(
                ticker, "buy", amount_to_buy, crypto_to_crypto_bid_price
            )["orderId"]
            order = private_client.get_order_details(order_id)
            is_live = order["isActive"]
            new_buy_counter = 6
            while is_live:
                order = private_client.get_order_details(order["id"])
                is_live = order["isActive"]
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
                    amount_to_buy = f"{Decimal(10) / price_in_usd:.5f}"
                    order_id = private_client.create_limit_order(
                        ticker, "buy", amount_to_buy, crypto_to_crypto_bid_price
                    )["orderId"]
                    order = private_client.get_order_details(order_id)
                    new_buy_counter = 6
                time.sleep(10)
                new_buy_counter -= 1

        print(f'Bought {order["size"]} amount of {ticker} for {order["price"]}')


def sell_order(ticker: str, amount: str, price: str):
    public_client = Market()
    private_client = Trade(
        key=config.kucoin_api_key,
        secret=config.kucoin_api_secret,
        passphrase=config.kucoin_api_passphrase,
    )
    if not price:
        price = public_client.get_ticker(ticker)["bestAsk"]
    order_id = private_client.create_limit_order(ticker, "sell", amount, price)[
        "orderId"
    ]
    order = private_client.get_order_details(order_id)
    print(f'Sold {order["size"]} amount of {ticker} for {order["price"]}')
