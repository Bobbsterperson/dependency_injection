import sqlite3

class SQLiteConnector:
    def __init__(self, db_name='example.db'):
        # Connect to the SQLite database (it will create the file if it doesn't exist)
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Create a table if it doesn't already exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_item(self, item):
        # Insert an item into the items table
        self.cursor.execute('INSERT INTO items (item) VALUES (?)', (item,))
        self.conn.commit()
        print(f'Added: {item}')  # Confirm the item is added
        print(f"Total items after addition: {self.cursor.lastrowid}")

    def display_items(self):
        # Query and display all items
        self.cursor.execute('SELECT * FROM items')
        rows = self.cursor.fetchall()
        print("\nCurrent items in the database:")
        for row in rows:
            print(row)

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
