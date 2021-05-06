import time
import schedule
from bot.cbpro import trader as cbpro_trader
from bot.gemini import trader as gemini_trader
from bot.kucoin import trader as kucoin_trader
import dca_portfolio


def main():
    if dca_portfolio.cbpro_portfolio:
        print("yup")
        pass
        #cbpro_trader.run_trades(dca_portfolio.cbpro_portfolio)
    if dca_portfolio.kucoin_portfolio:
        kucoin_trader.run_trades(dca_portfolio.kucoin_portfolio)
    if dca_portfolio.gemini_portfolio:
        pass
        #gemini_trader.run_trades(dca_portfolio.gemini_portfolio)


def auto_deposit():
    cbpro_trader.auto_deposit(dca_portfolio.cbpro_auto_deposit_amount)


def sell_order():
    ticker = input("Please enter the ticker of the crypto you would like to sell: ")
    amount = input("Please enter the amount of the crypto you would like to sell: ")
    price = input(
        "Please enter the price you would like to sell the crypto at (if you provide nothing it will be at the lowest current ask price): "
    )
    exchange = input(
        "Please enter the exchange you are selling on ('gemini', 'cbpro', 'kucoin'): "
    )
    if exchange == "gemini":
        gemini_trader.sell_order(ticker, amount, price)
    elif exchange == "cbpro":
        cbpro_trader.sell_order(ticker, amount, price)
    elif exchange == "kucoin":
        kucoin_trader.sell_order(ticker, amount, price)
    else:
        print("Only 'gemini', 'cbpro', or 'kucoin' is supported")


if __name__ == "__main__":
    user_input = input(
        "Please enter eitner 'schedule' to run a recurring job, 'run' to run a non-recurring job now or 'sell' to sell a position: "
    )
    if user_input == "schedule":
        print("Schedule job start, will DCA based on the specified time")
        schedule.every().sunday.at("13:00").do(main)
        schedule.every(4).weeks.do(auto_deposit)
        while True:
            schedule.run_pending()
            time.sleep(1)
    elif user_input == "run":
        main()
    elif user_input == "sell":
        sell_order()
    else:
        print(
            "Must provide an arguement value of either 'schedule' to schedule a recurring job, 'run' to run non-recurring job now or 'sell' to sell a position"
        )
