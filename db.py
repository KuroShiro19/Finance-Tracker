import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,             -- YYYY-MM-DD
    symbol TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('BUY','SELL','DIVIDEND','FEE','DEPOSIT','WITHDRAW')),
    quantity REAL DEFAULT 0,
    price REAL DEFAULT 0,
    fees REAL DEFAULT 0,
    currency TEXT DEFAULT 'USD',
    account TEXT DEFAULT 'main',
    notes TEXT
);
"""

def get_conn(path="portfolio.db"):
    conn = sqlite3.connect(path)
    conn.executescript(SCHEMA)
    return conn

def add_transaction(conn, date, symbol, type_, quantity=0, price=0,
                    fees=0, currency="USD", account="main", notes=""):
    conn.execute(
        "INSERT INTO transactions (date,symbol,type,quantity,price,fees,currency,account,notes) "
        "VALUES (?,?,?,?,?,?,?,?,?)",
        (date, symbol.upper(), type_.upper(), quantity, price, fees, currency, account, notes),
    )
    conn.commit()
