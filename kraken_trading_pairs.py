# This updated Function will only get viable trading pairs that exclude currency pairs when the initial quote currency is a currency. 



import json
import requests


def get_Asset_Pairs():
    AssetPairs = []
    response = requests.get('https://api.kraken.com/0/public/AssetPairs')
    results = response.json()
    for ticker_key, ticker_data in results["result"].items():
        AssetPairs.append({
            "symbol": ticker_key,
            "altname": ticker_data["altname"],
            "wsname": ticker_data['wsname'],
            "base": ticker_data['base'],
            "quote": ticker_data["quote"],
            "pair_decimals": ticker_data["pair_decimals"],
            "cost_decimals": ticker_data["cost_decimals"],
            "lot_decimals": ticker_data["lot_decimals"],
            "lot": ticker_data["lot"],
            "lot_multiplier": ticker_data["lot_multiplier"],
            "fees": ticker_data["fees"],
            "tick_size": ticker_data["tick_size"],
            "status": ticker_data["status"],
        })
    return AssetPairs

def get_trading_combinations(quote):
    AssetPairs = get_Asset_Pairs()
    combinations = []
    for ticker1 in AssetPairs:
        sym1_token1 = ticker1["base"]
        sym1_token2 = ticker1["quote"]
        symbol1 = ticker1["symbol"]
        fees1 = ticker1["fees"]
        status1 = ticker1["status"]
        lot_decimals1 = ticker1["lot_decimals"]
        cost_decimals1 =  ticker1["cost_decimals"]
        if status1 == "online":
            if ((sym1_token2 == f'Z{quote}') or (sym1_token2 == f'X{quote}') or (sym1_token2 == quote)) and (str(sym1_token1)[0] != 'Z'):
                for ticker2 in AssetPairs:
                    sym2_token1 = ticker2["base"]
                    sym2_token2 = ticker2["quote"]
                    symbol2 = ticker2["symbol"]
                    fees2 = ticker2["fees"]
                    status2 = ticker2["status"]
                    lot_decimals2 = ticker2["lot_decimals"]
                    cost_decimals2 = ticker2["cost_decimals"]
                    if (status2 == "online" and sym1_token1 == sym2_token2) and (str(sym2_token1)[0] != 'Z'):
                        for ticker3 in AssetPairs:
                            sym3_token1 = ticker3["base"]
                            sym3_token2 = ticker3["quote"]
                            symbol3 = ticker3["symbol"]
                            fees3 = ticker3["fees"]
                            status3 = ticker3["status"]
                            lot_decimals3 = ticker3["lot_decimals"]
                            cost_decimals3 = ticker3["cost_decimals"]
                            if status3 == "online" and sym2_token1 == sym3_token1 and sym3_token2 == sym1_token2:
                                combination = {
                                    'base': sym1_token2,
                                    "base_ticker": symbol1,
                                    "fees1": fees1,
                                    "lot_decimal_base": lot_decimals1,
                                    "cost_decimal_base": cost_decimals1,
                                    'intermediate': sym1_token1,
                                    "intermediate_ticker": symbol2,
                                    "fees2": fees2,
                                    "lot_decimal_intermediate": lot_decimals2,
                                    "cost_decimal_intermediate": cost_decimals2,
                                    'end': sym2_token1,
                                    "end_ticker": symbol3,
                                    "fees3": fees3,
                                    "lot_decimal_end": lot_decimals3,
                                    "cost_decimal_end": cost_decimals3,
                                }
                                combinations.append(combination)
    return combinations

ticker = input("Enter a valid Ticker: ").upper()

print(get_trading_combinations(ticker))

"""
with open(f'{ticker}_combinations_kraken.json', "w") as file:
    json.dump(get_trading_combinations(ticker), file, indent=4)
"""
