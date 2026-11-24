import pandas as pd
from db import add_transaction

def import_csv(conn, path):
    """Expected columns: date,symbol,type,quantity,price,fees,currency"""
    df = pd.read_csv(path)
    for r in df.itertuples():
        add_transaction(conn, r.date, r.symbol, r.type, r.quantity,
                        r.price, getattr(r, "fees", 0), getattr(r, "currency", "USD"))
