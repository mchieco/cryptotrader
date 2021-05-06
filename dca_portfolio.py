from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Coin:
    ticker: str
    buy_amount: Decimal

gemini_portfolio = [
    Coin("btcusd", 30), 
    Coin("ethusd", 30), 
    Coin("linkusd", 10)
]
cbpro_portfolio = [
    Coin("ALGO-USD", 10),
    Coin("ATOM-USD", 10)
]
kucoin_portfolio = [
    Coin("VET-BTC", 10)
]

cbpro_auto_deposit_amount = 25.00