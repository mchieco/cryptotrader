import time
from decimal import Decimal
from dca_portfolio import Coin
from cbpro import PublicClient, AuthenticatedClient
import config

def run_trades(coin_list: list[Coin]):
    public_client = PublicClient()
    authenticated_client = AuthenticatedClient(
        config.coinbase_pro_api_key, 
        config.coinbase_pro_api_secret, 
        config.coinbase_pro_api_passphrase,
    )
    for coin in coin_list:
        ticker = coin.ticker
        amount = coin.buy_amount
        print(public_client.get_product_ticker(ticker))
        bid_price = Decimal(public_client.get_product_ticker(ticker)['bid'])
        amount_to_buy = amount / bid_price
        order = authenticated_client.place_limit_order(product_id=ticker, size=str(f'{amount_to_buy:.6f}'), price=str(bid_price), side="buy")
        settled = order['settled']
        new_buy_counter = 6
        while not (settled):
            order = authenticated_client.get_order(order['id'])
            settled = order['settled']
            if(new_buy_counter < 1):
                authenticated_client.cancel_order(order['id'])
                print("canceled order")
                bid_price = Decimal(public_client.get_product_ticker(ticker)['bid'])
                order = authenticated_client.place_limit_order(product_id=ticker, size=str(f'{amount_to_buy:.6f}'), price=str(bid_price), side="buy")
                new_buy_counter = 6
            
            time.sleep(10)
            new_buy_counter -= 1

        print(f'Bought {order["original_amount"]} amount of {ticker} for {order["price"]}')


def auto_deposit():
    authenticated_client = AuthenticatedClient(
        config.coinbase_pro_api_key, 
        config.coinbase_pro_api_secret, 
        config.coinbase_pro_api_passphrase,
    )
    payment_methods = authenticated_client.get_payment_methods()
    bank_payment_id = payment_methods[0]["id"]
    deposit_response = authenticated_client.deposit(25.00, "USD", bank_payment_id)
    print(f'Deposited {deposit_response["amount"]} at {deposit_response["payout_at"]}')
