import sqlite3

class SQLiteConnector:
    def __init__(self, db_name='example.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL,
                processed INTEGER DEFAULT 0  -- 0 = unprocessed, 1 = processed
            )
        ''')
        self.conn.commit()

    def add_item(self, item):
        self.cursor.execute('INSERT INTO items (item, processed) VALUES (?, 0)', (item,))
        self.conn.commit()

    def display_items(self):
        self.cursor.execute('SELECT * FROM items WHERE processed = 0')
        rows = self.cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No unprocessed items to display.")

    def close(self):
        self.cursor.close()
        self.conn.close()

def main():
    sqlite_connector = SQLiteConnector()
    try:
        while True:
            item = input("Enter an item: ")
            if item.lower() == 'exit':
                break
            sqlite_connector.add_item(item)
            sqlite_connector.display_items()
    finally:
        sqlite_connector.close()

if __name__ == "__main__":
    main()
