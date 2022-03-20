from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Coin:
    ticker: str
    buy_amount: Decimal

gemini_portfolio = [
    Coin("btcusd", 10),
    Coin("ethusd", 40),
    Coin("linkusd", 20),
]
cbpro_portfolio = [
    Coin("DOT-USD", 10),
    Coin("ATOM-USD", 10),
    Coin("ADA-USD", 10),
]
kucoin_portfolio = [
]

cbpro_auto_deposit_amount = 50.00