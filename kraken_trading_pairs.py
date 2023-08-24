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


def get_Asset_Pairs():
    AssetPairs = []
    response = requests.get('https://api.kraken.com/0/public/AssetPairs')
    results = response.json()
    result = results.get('result')
    for i in result.keys():
        # print(i)
        AssetPairs.append({
            "altname": result[i]["altname"],
            "wsname": result[i]['wsname'],
            "base": result[i]['base'],
            "quote": result[i]["quote"],
            "pair_decimals": result[i]["pair_decimals"],
            "cost_decimals": result[i]["cost_decimals"],
            "lot_decimals": result[i]["lot_decimals"],
            "lot": result[i]["lot"],
            "lot_multiplier": result[i]["lot_multiplier"],
            "fees": result[i]["fees"],
            "tick_size": result[i]["tick_size"],
            "status": result[i]["status"],
        })
    return AssetPairs
print(get_Asset_Pairs())
"""AssetPairs = get_Asset_Pairs()"""

def get_trading_combinations(quote):
    AssetPairs = get_Asset_Pairs()
    combinations = []
    for ticker1 in AssetPairs:
        sym1_token1 = ticker1["base"]
        sym1_token2 = ticker1["quote"]
        symbol1 = ticker1["altname"]
        # stepSize1 = ticker1[""]
        fees1 = ticker1["fees"]
        # print(sym1_token1, sym1_token2)
        # print(type(sym1_token2))
        if (sym1_token2 == f'Z{quote}') or (sym1_token2 == f'X{quote}') or (sym1_token2 == quote):
            for ticker2 in AssetPairs:
                # Extract the 'symbol' value from the data

                sym2_token1 = ticker2["base"]
                sym2_token2 = ticker2["quote"]
                symbol2 = ticker2["altname"]
                # stepSize2 = ticker2["stepSize"]
                fees2 = ticker2["fees"]
                # print(sym2_token1, sym2_token2)

                if sym1_token1 == sym2_token2:
                    for ticker3 in AssetPairs:
                        # Extract the 'symbol' value from the data

                        sym3_token1 = ticker3["base"]
                        sym3_token2 = ticker3["quote"]
                        symbol3 = ticker3["altname"]
                        # stepSize3 = ticker3["stepSize"]
                        fees3 = ticker3["fees"]
                        if sym2_token1 == sym3_token1 and sym3_token2 == sym1_token2:
                            combination = {
                                'base': sym1_token2,
                                "base_ticker": symbol1,
                                "fees1": fees1,
                                # "base_ticker_stepSize": stepSize1,
                                'intermediate': sym1_token1,
                                "intermediate_ticker": symbol2,
                                "fees2": fees2,
                                # "intermediate_ticker_stepSize": stepSize2,
                                'end': sym2_token1,
                                "end_ticker": symbol3,
                                "fees3": fees3,
                                # "end_ticker_stepSize": stepSize3,

                            }
                            combinations.append(combination)

    return combinations

ticker = input("Enter a valid Ticker: ").upper()
with open(f'{ticker}_combinations_kraken.json', "w") as file:
    json.dump(get_trading_combinations(ticker), file)
