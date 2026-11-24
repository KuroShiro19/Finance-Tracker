import streamlit as st
from db import get_conn
from engine import load_transactions, compute_positions, add_market_value
from prices import latest_prices

st.title("My Portfolio")
conn = get_conn()
tx = load_transactions(conn)

if tx.empty:
    st.info("No transactions yet. Import a CSV or add one below.")
else:
    pos = compute_positions(tx)
    pos = add_market_value(pos, latest_prices(list(pos.index)))
    c1, c2, c3 = st.columns(3)
    c1.metric("Market value", f"{pos.market_value.sum():,.0f}")
    c2.metric("Unrealised P&L", f"{pos.unrealised_pnl.sum():,.0f}")
    c3.metric("Realised P&L", f"{pos.realised_pnl.sum():,.0f}")
    st.dataframe(pos.round(2))
    st.bar_chart(pos["weight_pct"])

with st.expander("Add transaction"):
    with st.form("tx"):
        d = st.date_input("Date")
        s = st.text_input("Symbol")
        t = st.selectbox("Type", ["BUY", "SELL", "DIVIDEND", "FEE"])
        q = st.number_input("Quantity", min_value=0.0)
        p = st.number_input("Price", min_value=0.0)
        f = st.number_input("Fees", min_value=0.0)
        if st.form_submit_button("Save"):
            from db import add_transaction
            add_transaction(conn, str(d), s, t, q, p, f)
            st.rerun()
