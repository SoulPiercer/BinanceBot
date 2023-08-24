def fetch_current_ticker_price(ticker):
    response = requests.get("https://api.kraken.com/0/public/Ticker")
    result = response.json()
    get_ticker_information = result.get('result')
    
    trading_pair_Combinations = []
    # unique_Tickers = []
    
    with open(f"{ticker}_combinations_kraken.json") as file:
        combinations = json.load(file)

    for trio in list(combinations):                                        # If more Variables are needed, Call Them here and add them to the output below ie.) decimal size
        arbitrage_trio = []
        
        base_ticker = trio["base_ticker"]
        intermediate_ticker = trio["intermediate_ticker"]
        end_ticker = trio["end_ticker"]
        fees1 = trio["fees1"]
        fees2 = trio["fees2"]
        fees3 = trio["fees3"]

        
        """
        unique_Tickers.append(base_ticker)
        unique_Tickers.append(intermediate_ticker)
        unique_Tickers.append(end_ticker)
        """

        for i in get_ticker_information.keys
            base_ticker_price = ""
            intermediate_ticker_price = ""
            end_ticker_price = ""
        
            if result[i] == base_ticker:
                base_ticker_a = result[i]['a']
                base_ticker_b = result[i]['b']
                base_ticker_price = result[i]['c']           # c = last trade closed
                base_ticker_v = result[i]['v']
                base_ticker_weightedV = result[i]['p']             # Volume weighted average price
                elif result[i] == intermediate_ticker:
                    intermediate_ticker_a = result[i]['a']
                    intermediate_ticker_b = result[i]['b']
                    intermediate_ticker_price = result[i]['c']
                    intermediate_ticker_v = result[i]['v']
                    intermediate_ticker_weightedV = result[i]['p']
                    elif result[i] == end_ticker:
                    end_ticker_a = result[i]['a']
                    end_ticker_b = result[i]['b']
                    end_ticker_price = result[i]['c']
                    end_ticker_v = result[i]['v']
                    end_ticker_weightedV = result[i]['p']

            if len(base_ticker_price) > 0 and len(intermediate_ticker_price) > 0 and len(end_ticker_price) > 0:            # Add more variables here as needed
            
                arbitrage_trio.append({
                    "base_ticker": base_ticker ,
                    "base_ask": base_ticker_a ,
                    "base_bid": base_ticker_b ,
                    "base_ticker_price": base_ticker_price,
                    "base_ticker_v": base_ticker_v,
                    "base_ticker_weightedV":base_ticker_weightedV ,
                    "base_fees": fees1
    
                    "intermediate_ticer": intermediate_ticker
                    "intermediate_ticker_a": intermediate_ticker_a ,
                    "intermediate_ticker_b": intermediate_ticker_b, 
                    "intermediate_ticker_price": intermediate_ticker_price, 
                    "intermediate_ticker_v": intermediate_ticker_v, 
                    "intermediate_ticker_weightedV": intermediate_ticker_weightedV ,
                    "intermediate_fees": fees2
                    
                    "end_ticker": end_ticker,
                    "end_ticker_a": end_ticker_a, 
                    "end_ticker_b": end_ticker_b,
                    "end_ticker_price": end_ticker_price ,
                    "end_ticker_v": end_ticker_v ,
                    "end_ticker_weightedV": end_ticker_weightedV,
                    "end_fees": fees3,
                    break
                    
                })
            else:
                continue

        trading_pair_Combinations.append(arbitrage_trio)
    return trading_pair_Combinations

print(fetch_current_ticker_price(USD))
        



# Reformat input for pricing Formula




# Triangle Arbitrage profit / loss calculations
def check_if_float_zero(value):
    return math.isclose(value, 0.0, abs_tol=1e-3)

def check_buy_buy_sell(initial_investment):
    buy_buy_sell = []
    trading_pair_Combinations = fetch_current_ticker_price("USDT")

    investment_amount = initial_investment
    for trio in trading_pair_Combinations:   # write a for loop to get the prices for each pair in each trio
        try:
            with open("trading-fees.json") as data_list:
                fees = json.load(data_list)

                ticker1 = requests.get(f"https://api.binance.us/api/v3/ticker?symbol={trio[0]['symbol']}").json()
                ticker2 = requests.get(f"https://api.binance.us/api/v3/ticker?symbol={trio[1]['symbol']}").json()
                ticker3 = requests.get(f"https://api.binance.us/api/v3/ticker?symbol={trio[2]['symbol']}").json()
                current_price1 = ticker1["lastPrice"]
                current_price2 = ticker2["lastPrice"]
                current_price3 = ticker3["lastPrice"]
                for ticker in fees:
                    if ticker['symbol'] == trio[0]['symbol']:
                        ticker1_fee = float(ticker["takerCommission"])
                    if ticker['symbol'] == trio[1]['symbol']:
                        ticker2_fee = float(ticker["takerCommission"])
                    if ticker['symbol'] == trio[2]['symbol']:
                        ticker3_fee = float(ticker["takerCommission"])

                # print(current_price1,current_price2,current_price3)

                trade1_before_fee = (1 / float(current_price1)) * investment_amount
                trade1 = trade1_before_fee - (trade1_before_fee * ticker1_fee)

                trade2_before_fee = trade1 / float(current_price2)
                trade2 = trade2_before_fee - (trade2_before_fee * ticker2_fee)
                trade3_before_fee = trade2 * float(current_price3)
                trade3 = trade3_before_fee - (trade3_before_fee * ticker3_fee)

                final_price = trade3
                p_l = final_price - investment_amount
                p_l_percent = (p_l / investment_amount) * 100
                # print(final_price)
                trades = {
                    "Symbol1": trio[0]['symbol'],
                    "Trade1": current_price1,
                    "step1": trio[0]['stepSize'],
                    "Symbol2": trio[1]['symbol'],
                    "Trade2": current_price2,
                    "step2": trio[1]['stepSize'],
                    "Symbol3": trio[2]['symbol'],
                    "Trade3": current_price3,
                    "step3": trio[2]["stepSize"],
                    "Profit/loss": p_l,
                    "P/L %": p_l_percent,
                    "Final Amount": final_price
                    }
                buy_buy_sell.append(trades)

        # print(scrip_prices)
        except requests.RequestException as e:
            print("An error occurred during the API request:", e)
            continue
        except KeyError as e:
            print("A key error occurred:", e)
            continue

        except Exception as e:
            print("An unexpected error occurred:", e)
            continue
    return buy_buy_sell

print(pd.DataFrame(check_buy_buy_sell(0.34)))
