from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Coin:
    ticker: str
    buy_amount: Decimal

gemini_portfolio = [
    Coin("btcusd", 10),
    Coin("ethusd", 20),
    Coin("linkusd", 20),
]
cbpro_portfolio = [
    Coin("DOT-USD", 20),
    Coin("ATOM-USD", 20),
    Coin("ALGO-USD", 5),
    Coin("ADA-USD", 5),
]
kucoin_portfolio = [
]

cbpro_auto_deposit_amount = 50.00