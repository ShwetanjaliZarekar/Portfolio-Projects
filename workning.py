
import sqlite3

con = sqlite3.connect('GitHub.db')
cur = con.cursor()
table_list = [a[0] for a in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]

for table_name in table_list:
    count = cur.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    print(f"{table_name}: {count} records")

con.close()

