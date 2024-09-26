import sqlite3
from abc import ABC, abstractmethod

class BundleStorage(ABC):
    @abstractmethod
    def create_bundle_table(self):
        pass

    @abstractmethod
    def insert_bundled_items(self, items: str):
        pass

class SQLiteBundleStorage(BundleStorage):
    def create_bundle_table(self):
        conn = sqlite3.connect("bundle.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS bundled_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            items TEXT NOT NULL
        )''')
        conn.commit()
        conn.close()

    def insert_bundled_items(self, items: str):
        conn = sqlite3.connect("bundle.db")
        cursor = conn.cursor()
        cursor.execute('INSERT INTO bundled_items (items) VALUES (?)', (items,))
        conn.commit()
        conn.close()

def bundle_items(database_path: str, table_name: str, bundle_storage: BundleStorage):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    query = f"SELECT * FROM {table_name} WHERE processed = 0;"

    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            print(f"No unprocessed items found in table '{table_name}'.")
            return

        num_complete_bundles = len(rows) // 5
        
        if num_complete_bundles == 0:
            print("Not enough unprocessed items to create a complete bundle of 5.")
            return

        for i in range(num_complete_bundles):
            bundle = rows[i * 5:(i + 1) * 5]
            bundled_items = [item[1] for item in bundle]
            items_str = ', '.join(bundled_items)
            print(f"Bundling items: {items_str}")

            bundle_storage.insert_bundled_items(items_str)

            item_ids = [item[0] for item in bundle]
            cursor.execute(f"UPDATE {table_name} SET processed = 1 WHERE id IN ({', '.join('?' for _ in item_ids)})", item_ids)
            conn.commit()

        print(f"{num_complete_bundles} complete bundle(s) of unprocessed items added to 'bundle.db'.")

    except sqlite3.Error as e:
        print(f"Error reading from SQLite database: {e}")
    finally:
        conn.close()

def run_bundler():
    database_path = "example.db"
    table_name = "items"
    bundle_storage = SQLiteBundleStorage()
    bundle_storage.create_bundle_table()
    bundle_items(database_path, table_name, bundle_storage)