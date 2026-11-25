import numpy as np
from scipy.optimize import brentq

def max_drawdown(series):
    peak = series.cummax()
    return ((series - peak) / peak).min()