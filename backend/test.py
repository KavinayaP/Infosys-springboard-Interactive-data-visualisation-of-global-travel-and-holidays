import sqlite3

conn = sqlite3.connect("app.db")
cur = conn.cursor()

cur.execute("SELECT * FROM users")
rows = cur.fetchall()

for r in rows:
    print(r)
