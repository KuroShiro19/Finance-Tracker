import pandas as pd

def load_transactions(conn):
    return pd.read_sql("SELECT * FROM transactions ORDER BY date, id", conn, parse_dates=["date"])

def compute_positions(tx):
    positions, realised = {}, {}
    for r in tx.itertuples():
        if r.type not in ("BUY", "SELL"):
            continue
        p = positions.setdefault(r.symbol, {"qty": 0.0, "cost": 0.0})
        realised.setdefault(r.symbol, 0.0)
        if r.type == "BUY":
            p["qty"] += r.quantity
            p["cost"] += r.quantity * r.price + r.fees
        else:
            avg = p["cost"] / p["qty"] if p["qty"] else 0
            realised[r.symbol] += r.quantity * (r.price - avg) - r.fees
            p["qty"] -= r.quantity
            p["cost"] -= avg * r.quantity
    df = pd.DataFrame(positions).T
    df["avg_cost"] = df["cost"] / df["qty"].replace(0, float("nan"))
    df["realised_pnl"] = pd.Series(realised)
    return df[df["qty"] > 1e-9].join(df[["realised_pnl"]], rsuffix="_")

def add_market_value(pos, prices):
    pos = pos.copy()
    pos["price"] = prices.reindex(pos.index)
    pos["market_value"] = pos["qty"] * pos["price"]
    pos["unrealised_pnl"] = pos["market_value"] - pos["cost"]
    pos["return_pct"] = pos["unrealised_pnl"] / pos["cost"] * 100
    pos["weight_pct"] = pos["market_value"] / pos["market_value"].sum() * 100
    return pos
