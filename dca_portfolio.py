from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Coin:
    ticker: str
    buy_amount: Decimal

gemini_portfolio = [Coin("btcusd", Decimal(40)), Coin("ethusd", Decimal(30)), Coin("linkusd", Decimal(10))]
cbpro_portfolio = [Coin("ADA-USD", Decimal(10)), Coin("ALGO-USD", Decimal(10))]
kucoin_portfolio = [Coin("VET-BTC", Decimal(10))]