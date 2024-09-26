import sqlite3
from collections import Counter

"""
previosly i established a conection to a database and tore it down aftrer reading data,
the point of using singleton pattern here is that if my script gets more complex and it needs to open and close 
the database multiple times that would be recourse hungry. now i create an instance of the connection so it can be reused
in different places.
i implemented it in sqlite_manage.py also.
"""

class DatabaseConnection:
    _instance = None

    def __new__(cls, db_name):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.conn = sqlite3.connect(db_name)
            cls._instance.cursor = cls._instance.conn.cursor()
        return cls._instance

    def close(self):
        if self._instance:
            self._instance.conn.close()
            DatabaseConnection._instance = None

def get_bundles_from_db(db_connection):
    cursor = db_connection.cursor
    cursor.execute("SELECT items FROM bundled_items")
    bundled_items = cursor.fetchall()
    cursor.execute("SELECT items FROM bundled_items")
    items = cursor.fetchall()
    return [bundle[0].split(",") for bundle in bundled_items], [item[0] for item in items]

def count_word_occurrences(bundles, items):
    all_words = [word.strip() for bundle in bundles for word in bundle] + items
    return Counter(all_words)

def matchy():
    db_name = 'bundle.db'
    db_connection = DatabaseConnection(db_name)
    
    try:
        bundles, items = get_bundles_from_db(db_connection)
        word_counts = count_word_occurrences(bundles, items)
        for word, count in word_counts.items():
            if count > 1:
                print(f"Word: '{word}' occurs {count} times.")
    finally:
        db_connection.close()

if __name__ == "__main__":
    matchy()
