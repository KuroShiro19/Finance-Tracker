import numpy as np
from scipy.optimize import brentq

def xirr(cashflows):
    """cashflows: list of (datetime, amount); negative = money in, positive = money out/final value."""
    t0 = cashflows[0][0]
    f = lambda r: sum(a / (1 + r) ** ((d - t0).days / 365) for d, a in cashflows)
    return brentq(f, -0.99, 10)

def max_drawdown(series):
    peak = series.cummax()
    return ((series - peak) / peak).min()

def sharpe(returns, rf=0.03, periods=252):
    excess = returns - rf / periods
    return np.sqrt(periods) * excess.mean() / excess.std()
