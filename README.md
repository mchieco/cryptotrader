# Crypto Trader

Crypto Trader is a Python library for Dollar Cost Averaging Crypto, with some other API driven abilties as well.

## Installation

Clone the git repository.

Make sure you have python 3 installed on your machine, this can be done via homebrew.

Make sure you have [pip](https://pip.pypa.io/en/stable/) installed on your machine.

Make sure you have venv installed on your machine, this can be done via:

```bash
pip install venv
```

Once you have venv installed, you have to create a virtual environment in project folder.
This can be done by running the following command

```bash
python -m venv venv
```

Then you need to activate the venv, this can be done using the via:

```bash
source venv/bin/activate
```

Once you are in the venv, you can now install the project dependencies.

Run the following command from the root directory of the project in the venv:

```bash
pip install -r requirements.txt
```

Once you have done this, it is all set up and ready to be used!
Don't forget, you will need to be in the venv everytime you want to run the program.

## Usage

There are multiple ways to use this bot.
The 2 main features are the DCA scheduled buy, which is set by default to Sunday at 1pm; and the one time run which will buy the specified porfolio at runtime.

To run the scheduled job, it requires the server/computer its running on to always be on and running the script.
Therefore, if you don't have a server or raspberry pi, the single time run will be the best option.

In order to run the prgram run the following:
```bash
python -m bot
```
It will ask you what type of job you want to run, the keywords are ```schedule```, ```run```, or ```sell```  

You can also use the program to do singular sells through the API. This can save on transaction fees if they are lower on the API than on the platform, ex. Gemini.
The sell command will ask you questions about what you want to sell, so follow the promopts and it will fill out a sell limit order based on the inputs.

## Configuration

The program requires you to create a ```config.py``` file in the root directory.
This will contain all of your api keys, passphrases and secrets for all the platforms.

The config file must follow the same structure as it relies on the names of the coniguration elements to run properly.
Change the empty strings with your api secrets 
```python
#for gemini
gemini_api_key = ""
gemini_api_secret = ""
#for coinbase pro
coinbase_pro_api_key = ""
coinbase_pro_api_passphrase = ""
coinbase_pro_api_secret = ""
#for kucoin
kucoin_api_key = ""
kucoin_api_passphrase = ""
kucoin_api_secret = ""
```

## Portfolio

The other piece of information that is required is the crypto you want to buy and the amount in USD you want to buy of it.
This is done in the ```dca_portfolio.py``` file in the root directory.
You simply add the ticker value and the amount of money you want to invest per run per coin.
There is also the ability to auto deposit into coinbase pro at the same time if you so choose, this can be done via adding:

```python
cbpro_auto_deposit_amount = 25.00
```

You will also need to select yes when it asks you if you want to autodeposit on a scheduled job.


By creating a coin in the portfolio following the structure below, it will place a limit buy at the highest current bid, and then wait until the order is filled to move on to the next order. If the order isn't filled within a minute, then it will cancel the order and create a new order at the current highest bid.

```python
gemini_portfolio = [
    Coin("btcusd", 30), 
    Coin("ethusd", 30)
]
cbpro_portfolio = [
    Coin("ALGO-USD", 10),
    Coin("ATOM-USD", 10)
]
kucoin_portfolio = [
    Coin("VET-BTC", 10)
]
```

So in this example, it will buy $30 in btc, $30 in eth, $10 in ALGO, $10 in ATOM, and $10 in VET.
If you are not investing on one of the platforms simply remove all the Coin objects from the portfolio

```python
gemini_portfolio = [ #not using gemini 
]
cbpro_portfolio = [ #using cbpro
    Coin("ALGO-USD", 10),
    Coin("ATOM-USD", 10)
]
kucoin_portfolio = [ #using kucoin
    Coin("VET-BTC", 10)
]
```

## Final Thoughts

Once you have the config setup and the dca portfolio to your liking, this will auto invest as you choose to take the emotion out of buying crypto. It will also reduce the fees as some exchanges have lower fees for API's.

Please feel free to make changes off this and customize the buying to your liking. Just wanted to build something to help simplify my strategy, so I hope it can help others out too.
