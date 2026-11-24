import yfinance as yf
import pandas as pd

def get_prices(symbols, start="2020-01-01"):
    data = yf.download(list(symbols), start=start, auto_adjust=True, progress=False)["Close"]
    if isinstance(data, pd.Series):
        data = data.to_frame(symbols[0])
    return data.ffill()

def latest_prices(symbols):
    return get_prices(symbols, start=(pd.Timestamp.today() - pd.Timedelta(days=10)).strftime("%Y-%m-%d")).iloc[-1]
