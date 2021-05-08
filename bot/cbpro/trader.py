import time
from decimal import Decimal
from cbpro import PublicClient, AuthenticatedClient
from dca_portfolio import Coin
import config


def run_trades(coin_list: list[Coin]):
    public_client = PublicClient()
    for coin in coin_list:
        authenticated_client = AuthenticatedClient(
            config.coinbase_pro_api_key,
            config.coinbase_pro_api_secret,
            config.coinbase_pro_api_passphrase,
        )
        ticker = coin.ticker
        amount = coin.buy_amount
        if ticker.split("-")[1] == ("USD" or "USDC"):
            bid_price = Decimal(public_client.get_product_ticker(ticker)["bid"])
            amount_to_buy = amount / bid_price
            order = authenticated_client.place_limit_order(
                product_id=ticker,
                size=str(f"{amount_to_buy:.6f}"),
                price=str(bid_price),
                side="buy",
            )
            settled = order["settled"]
            new_buy_counter = 6
            while not settled:
                order = authenticated_client.get_order(order["id"])
                settled = order["settled"]
                if new_buy_counter < 1:
                    authenticated_client.cancel_order(order["id"])
                    print(f"canceled order with id {order['id']}")
                    bid_price = Decimal(public_client.get_product_ticker(ticker)["bid"])
                    order = authenticated_client.place_limit_order(
                        product_id=ticker,
                        size=str(f"{amount_to_buy:.6f}"),
                        price=str(bid_price),
                        side="buy",
                    )
                    new_buy_counter = 6

                time.sleep(10)
                new_buy_counter -= 1
        else:
            crypto_to_crypto_bid_price = public_client.get_product_ticker(ticker)["bid"]
            usd_price = public_client.get_product_ticker(f"{ticker.split('-')[1]}-USD")[
                "price"
            ]
            price_in_usd = Decimal(crypto_to_crypto_bid_price) * Decimal(usd_price)
            amount_to_buy = Decimal(10) / price_in_usd
            order = authenticated_client.place_limit_order(
                product_id=ticker,
                size=str(f"{amount_to_buy:.6f}"),
                price=str(crypto_to_crypto_bid_price),
                side="buy",
            )
            settled = order["settled"]
            new_buy_counter = 6
            while not settled:
                order = authenticated_client.get_order(order["id"])
                settled = order["settled"]
                if new_buy_counter < 1:
                    authenticated_client.cancel_order(order["id"])
                    print(f"canceled order with id {order['id']}")
                    crypto_to_crypto_bid_price = public_client.get_product_ticker(
                        ticker
                    )["bid"]
                    usd_price = public_client.get_product_ticker(
                        f"{ticker.split('-')[1]}-USDT"
                    )["price"]
                    price_in_usd = Decimal(crypto_to_crypto_bid_price) * Decimal(
                        usd_price
                    )
                    amount_to_buy = Decimal(10) / price_in_usd
                    order = authenticated_client.place_limit_order(
                        product_id=ticker,
                        size=str(f"{amount_to_buy:.6f}"),
                        price=str(crypto_to_crypto_bid_price),
                        side="buy",
                    )
                    new_buy_counter = 6
                time.sleep(10)
                new_buy_counter -= 1

        print(f'Bought {order["size"]} amount of {ticker} for {order["price"]}')


def sell_order(ticker: str, amount: str, price: str):
    public_client = PublicClient()
    authenticated_client = AuthenticatedClient(
        config.coinbase_pro_api_key,
        config.coinbase_pro_api_secret,
        config.coinbase_pro_api_passphrase,
    )
    if not price:
        price = public_client.get_product_ticker(ticker)["ask"]
    order = authenticated_client.place_limit_order(
        product_id=ticker,
        size=amount,
        price=price,
        side="sell",
    )
    print(f'Sold {order["size"]} amount of {ticker} for {order["price"]}')


def auto_deposit(amount: float):
    authenticated_client = AuthenticatedClient(
        config.coinbase_pro_api_key,
        config.coinbase_pro_api_secret,
        config.coinbase_pro_api_passphrase,
    )
    payment_methods = authenticated_client.get_payment_methods()
    bank_payment_id = payment_methods[0]["id"]
    deposit_response = authenticated_client.deposit(amount, "USD", bank_payment_id)
    print(f'Deposited {deposit_response["amount"]} at {deposit_response["payout_at"]}')
