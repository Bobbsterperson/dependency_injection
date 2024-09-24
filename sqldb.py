import sqlite3
conn = sqlite3.connect('sqlite.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL
    )
''')
items = []
cursor.executemany('INSERT INTO items (item) VALUES (?)', [(item,) for item in items])
conn.commit()
cursor.execute('SELECT * FROM items')
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
