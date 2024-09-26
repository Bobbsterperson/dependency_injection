import sqlite3
from abc import ABC, abstractmethod
from sql_build import SQLBuilder

class BundleStorage(ABC):
    @abstractmethod
    def create_bundle_table(self):
        pass

    @abstractmethod
    def insert_bundled_items(self, items: str):
        pass

class SQLiteBundleStorage(BundleStorage):
    def __init__(self, db_name="bundle.db"):
        self.db_name = db_name
        self.create_bundle_table()

    def create_bundle_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS bundled_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            items TEXT NOT NULL
        )''')
        conn.commit()
        conn.close()

    def insert_bundled_items(self, items: str):
        sql_builder = SQLBuilder()
        query, params = sql_builder.insert("bundled_items", ["items"]).values(items).build()
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

def bundle_items(database_path: str, table_name: str, bundle_storage: BundleStorage):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    sql_builder = SQLBuilder()
    query, params = sql_builder.select("*", table_name, "processed = 0").build()
    cursor.execute(query, params)
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
        sql_builder = SQLBuilder()
        query, params = sql_builder.update(table_name, 
                                           "processed = 1", 
                                           f"id IN ({', '.join('?' for _ in item_ids)})").values(*item_ids).build()
        cursor.execute(query, params)
        conn.commit()
    print(f"{num_complete_bundles} complete bundle")
    conn.close()

def run_bundler():
    database_path = "example.db"
    table_name = "items"
    bundle_storage = SQLiteBundleStorage()
    bundle_items(database_path, table_name, bundle_storage)

if __name__ == "__main__":
    run_bundler()