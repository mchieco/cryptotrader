import schedule
import time
from bot.cbpro import trader as cbpro_trader
from bot.gemini import trader as gemini_trader
from bot.kucoin import trader as kucoin_trader
import dca_portfolio

def main():
    cbpro_trader.run_trades(dca_portfolio.cbpro_portfolio)
    kucoin_trader.run_trades()
    gemini_trader.run_trades(dca_portfolio.gemini_portfolio)


def auto_deposit():
    cbpro_trader.auto_deposit()


if __name__ == "__main__":
    schedule.every().sunday.at("13:00").do(main)
    schedule.every(4).weeks.do(auto_deposit)
    while True:
        schedule.run_pending()
        time.sleep(1)
    
