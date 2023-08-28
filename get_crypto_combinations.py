## Binance Crypto Combinations

import json
import math
import time
from datetime import datetime
import pandas as pd
from binance.spot import Spot as Client
from testnet_functions import binance_testnet
import urllib.parse
import hashlib
import hmac
import requests

api_url = 'https://api.binance.us/api/v3/exchangeInfo'

try:
    # Make an HTTP GET request to the API
    response = requests.get(api_url)
    # print(response.json())
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        json_data = response.json()

        # Extract the symbols list from the JSON data
        symbols_list = json_data.get('symbols', [])
        status_tickers = []
        # Iterate through the symbols list and extract baseAsset and quoteAsset
        for symbol_info in symbols_list:
            symbol = symbol_info.get('symbol')
            base_asset = symbol_info.get('baseAsset')
            quote_asset = symbol_info.get('quoteAsset')
            status = symbol_info.get('status')
            filters = symbol_info.get("filters")
            for filter in filters:
                if filter["filterType"] == "LOT_SIZE":
                    stepSize = (filter["stepSize"])

            if status == "TRADING":
                status_tickers.append({
                    'ticker': symbol,
                    "base_asset": base_asset,
                    "quote_asset": quote_asset,
                    "status": status,
                    "stepSize": stepSize
                })
            else:
                pass

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Error during API request: {e}")
except ValueError as ve:
    print(f"Error parsing JSON response: {ve}")


# Get unique combinations of currencies

def get_crypto_combinations(base):                                          #The Functions up to this point are redundant and need to be run once, then added to a file.
                                                                            # It is too compuationally expensive to run this everytime I need to call one of the function later in the program.
    combinations = []
   # tickerList =
    for ticker1 in status_tickers:                     # Rewrite this function to parse status_tickers output for tokens instead of using Tickers

        sym1_token1 = ticker1["base_asset"]
        sym1_token2 = ticker1["quote_asset"]
        symbol1 = ticker1["ticker"]
        stepSize1 = ticker1["stepSize"]
        # print(sym1_token1, sym1_token2)
        if sym1_token2 == base:
            for ticker2 in status_tickers:
                # Extract the 'symbol' value from the data

                sym2_token1 = ticker2["base_asset"]
                sym2_token2 = ticker2["quote_asset"]
                symbol2 = ticker2["ticker"]
                stepSize2 = ticker2["stepSize"]
                # print(sym2_token1, sym2_token2)


                if sym1_token1 == sym2_token2:
                    for ticker3 in status_tickers:
                        # Extract the 'symbol' value from the data

                        sym3_token1 = ticker3["base_asset"]
                        sym3_token2 = ticker3["quote_asset"]
                        symbol3 = ticker3["ticker"]
                        stepSize3 = ticker3["stepSize"]
                        if sym2_token1 == sym3_token1 and sym3_token2 == sym1_token2:
                            combination = {
                                'base': sym1_token2,
                                "base_ticker": symbol1,
                                "base_ticker_stepSize": stepSize1,
                                'intermediate': sym1_token1,
                                "intermediate_ticker": symbol2,
                                "intermediate_ticker_stepSize": stepSize2,
                                'end': sym2_token1,
                                "end_ticker": symbol3,
                                "end_ticker_stepSize": stepSize3,

                            }
                            combinations.append(combination)


    return combinations

ticker = input("Enter a valid Ticker: ").upper()
with open(f'{ticker}_combinations.json', "w") as file:
    json.dump(get_crypto_combinations(ticker), file)
