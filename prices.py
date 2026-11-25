import yfinance as yf
import pandas as pd

def get_prices(symbols, start="2020-01-01"):
    data = yf.download(list(symbols), start=start, auto_adjust=True, progress=False)["Close"]
    #Downloads data from Yahoo Finance for the given symbols and start date, and selects the 'Close' prices adjusted for events.
    if isinstance(data, pd.Series):
        data = data.to_frame(symbols[0])
    return data.ffill()

def latest_prices(symbols):
    symbols = list(symbols)
    if not symbols:
        return pd.Series(dtype="float64")

    data = get_prices(symbols, start=(pd.Timestamp.today() - pd.Timedelta(days=10)).strftime("%Y-%m-%d"))
    if data.empty:
        raise ValueError(f"No price data returned for: {', '.join(symbols)}")
    return data.iloc[-1]
