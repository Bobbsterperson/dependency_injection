import sqlite3
from abc import ABC, abstractmethod
from mach import matchy
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
    _instance = None  # This will hold the single instance of the class
    
    def __new__(cls, db_name='example.db'):
        if cls._instance is None:
            print("Creating new SQLiteItemStorage instance")
            cls._instance = super(SQLiteItemStorage, cls).__new__(cls)
            cls._instance.conn = sqlite3.connect(db_name)
            cls._instance.cursor = cls._instance.conn.cursor()
            cls._instance.create_table()
        return cls._instance

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
        if self._instance:
            self.cursor.close()
            self.conn.close()
            SQLiteItemStorage._instance = None  # Reset the instance so a new one can be created later

def main():
    item_storage = SQLiteItemStorage()  # This will always return the same instance of SQLiteItemStorage
    try:
        while True:
            item = input("Enter an item: ")
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
        item_storage.close()  # Close the connection at the end of the script
    run_bundler()
    matchy()

if __name__ == "__main__":
    main()
