import sqlite3
DB = "products.db"
with sqlite3.connect(DB) as db:
    db.execute("""CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL
                )""")
print("DB initialised")
