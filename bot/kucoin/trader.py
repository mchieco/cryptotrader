from kucoin.client import Market, Trade

def run_trades():
    public_client = Market(url='https://api.kucoin.com')
    data = public_client.get_ticker("VET-BTC")
    print(data)
