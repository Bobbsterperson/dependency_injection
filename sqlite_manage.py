import sqlite3
from abc import ABC, abstractmethod
from bundler import run_bundler

class ItemStorage(ABC):
    @abstractmethod
    def add_item(self, item: str):
        pass

    @abstractmethod
    def get_unprocessed_items(self):
        pass

    @abstractmethod
    def close(self):
        pass

class SQLiteItemStorage(ItemStorage):
    def __init__(self, db_name='example.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            processed INTEGER DEFAULT 0
        )''')
        self.conn.commit()

    def add_item(self, item: str):
        self.cursor.execute('INSERT INTO items (item, processed) VALUES (?, 0)', (item,))
        self.conn.commit()

    def get_unprocessed_items(self):
        self.cursor.execute('SELECT * FROM items WHERE processed = 0')
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

def main():
    item_storage = SQLiteItemStorage()
    try:
        while True:
            item = input("Enter an item (or type 'exit' to finish): ")
            if item.lower() == 'exit':
                break
            item_storage.add_item(item)
            unprocessed_items = item_storage.get_unprocessed_items()
            if unprocessed_items:
                for row in unprocessed_items:
                    print(row)
            else:
                print("No unprocessed items to display.")
    finally:
        item_storage.close()
    run_bundler()

if __name__ == "__main__":
    main()
