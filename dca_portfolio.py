from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Coin:
    ticker: str
    buy_amount: Decimal

gemini_portfolio = [
    Coin("btcusd", 40), 
    Coin("ethusd", 20),
    Coin("linkusd", 10)
]
cbpro_portfolio = [
]
kucoin_portfolio = [
    Coin("VET-BTC", 5),
    Coin("ALGO-BTC", 5),
    Coin("ATOM-BTC", 10),
    Coin("ADA-BTC", 10),
]

cbpro_auto_deposit_amount = 25.00