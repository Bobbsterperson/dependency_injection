import sqlite3
from collections import Counter

def get_bundles_from_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT items FROM bundled_items")
    bundled_items = cursor.fetchall()
    cursor.execute("SELECT items FROM bundled_items")
    items = cursor.fetchall()
    conn.close()
    return [bundle[0].split(",") for bundle in bundled_items], [item[0] for item in items]

def count_word_occurrences(bundles, items):
    all_words = [word.strip() for bundle in bundles for word in bundle] + items
    return Counter(all_words)

def matchy():
    db_name = 'bundle.db'
    bundles, items = get_bundles_from_db(db_name)
    word_counts = count_word_occurrences(bundles, items)
    for word, count in word_counts.items():
        if count > 1:
            print(f"Word: '{word}' occurs {count} times.")

if __name__ == "__main__":
    matchy()
