from decimal import Decimal
import time
from dca_portfolio import Coin
from gemini import PublicClient, PrivateClient
import config

def run_trades(coin_list: list[Coin]):
    public_client = PublicClient()
    private_client = PrivateClient(config.gemini_api_key, config.gemini_api_secret)
    for coin in coin_list:
        ticker = coin.ticker
        amount = coin.buy_amount
        bid_price = Decimal(public_client.get_ticker(ticker)['bid'])
        amount_to_buy = amount / bid_price
        order = private_client.new_order(ticker, str(f'{amount_to_buy:.6f}'), str(bid_price), "buy", [])
        is_live = order['is_live']
        new_buy_counter = 6
        while (is_live):
            order = private_client.status_of_order(order['order_id'])
            is_live = order['is_live']
            if(new_buy_counter < 1):
                private_client.cancel_order(order['order_id'])
                print("canceled order")
                bid_price = Decimal(public_client.get_ticker(ticker)['bid'])
                order = private_client.new_order(ticker, str(f'{amount_to_buy:.6f}'), str(bid_price), "buy", [])
                new_buy_counter = 6
            
            time.sleep(10)
            new_buy_counter -= 1
        
        print(f'Bought {order["original_amount"]} amount of {ticker} for {order["price"]}')
        