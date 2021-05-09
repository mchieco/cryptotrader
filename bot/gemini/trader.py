from decimal import Decimal
import time
from gemini import PublicClient, PrivateClient
from dca_portfolio import Coin
import config


def run_trades(coin_list: list[Coin]):
    public_client = PublicClient()
    for coin in coin_list:
        private_client = PrivateClient(config.gemini_api_key, config.gemini_api_secret)
        ticker = coin.ticker
        amount = coin.buy_amount
        precision_value = _get_precision_value(public_client, ticker)
        if ticker[-3:] == ("usd"):
            bid_price = Decimal(public_client.get_ticker(ticker)["bid"])
            amount_to_buy = amount / bid_price
            order = private_client.new_order(
                ticker,
                str(f"{amount_to_buy:.{precision_value}f}"),
                str(bid_price),
                "buy",
                [],
            )
            is_live = order["is_live"]
            new_buy_counter = 6
            while is_live:
                order = private_client.status_of_order(order["order_id"])
                is_live = order["is_live"]
                if new_buy_counter < 1:
                    private_client.cancel_order(order["order_id"])
                    print(f"canceled order with id {order['order_id']}")
                    bid_price = Decimal(public_client.get_ticker(ticker)["bid"])
                    order = private_client.new_order(
                        ticker,
                        str(f"{amount_to_buy:.{precision_value}f}"),
                        str(bid_price),
                        "buy",
                        [],
                    )
                    new_buy_counter = 6

                time.sleep(10)
                new_buy_counter -= 1
        else:
            crypto_to_crypto_bid_price = public_client.get_ticker(ticker)["bid"]
            usd_price = public_client.get_ticker(f"{ticker[-3:]}usd")["price"]
            price_in_usd = Decimal(crypto_to_crypto_bid_price) * Decimal(usd_price)
            amount_to_buy = Decimal(10) / price_in_usd
            order = private_client.new_order(
                ticker,
                str(f"{amount_to_buy:.{precision_value}f}"),
                str(crypto_to_crypto_bid_price),
                "buy",
                [],
            )
            is_live = order["is_live"]
            new_buy_counter = 6
            while is_live:
                order = private_client.status_of_order(order["order_id"])
                is_live = order["is_live"]
                if new_buy_counter < 1:
                    private_client.cancel_order(order["order_id"])
                    print(f"canceled order with id {order['order_id']}")
                    crypto_to_crypto_bid_price = public_client.get_ticker(ticker)["bid"]
                    usd_price = public_client.get_ticker(f"{ticker[-3:]}usd")["bid"]
                    price_in_usd = Decimal(crypto_to_crypto_bid_price) * Decimal(
                        usd_price
                    )
                    amount_to_buy = Decimal(10) / price_in_usd
                    order = private_client.new_order(
                        ticker,
                        str(f"{amount_to_buy:.{precision_value}f}"),
                        str(crypto_to_crypto_bid_price),
                        "buy",
                        [],
                    )
                    new_buy_counter = 6
                time.sleep(10)
                new_buy_counter -= 1

        print(
            f'Bought {order["original_amount"]} amount of {ticker} for {order["price"]}'
        )


def _get_precision_value(public_client: PublicClient, symbol: str) -> int:
    symbol_details = public_client.symbol_details(symbol)
    tick_size = str(symbol_details["tick_size"])
    if tick_size.startswith("1e"):
        return int(tick_size.split("-")[1])
    return len(tick_size.split(".")[1])


def sell_order(ticker: str, amount: str, price: str):
    public_client = PublicClient()
    private_client = PrivateClient(config.gemini_api_key, config.gemini_api_secret)
    if not price:
        price = public_client.get_ticker(ticker)["ask"]
    order = private_client.new_order(ticker, amount, price, "sell", [])
    print(f'Sold {order["original_amount"]} amount of {ticker} for {order["price"]}')
