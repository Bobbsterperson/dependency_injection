import sqlite3

def create_bundle_table():
    # Connect to the bundle.db database
    conn = sqlite3.connect("bundle.db")
    cursor = conn.cursor()

    # Create a new table to store the bundled items if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bundled_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            items TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def bundle_items(database_path: str, table_name: str):
    # Connect to the original database to fetch unprocessed items
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Fetch unprocessed items (where processed = 0)
    query = f"SELECT * FROM {table_name} WHERE processed = 0;"
    
    bundle_conn = None  # Initialize bundle_conn to None
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            print(f"No unprocessed items found in table '{table_name}'.")
            return

        # Count how many complete bundles of 5 can be created
        num_complete_bundles = len(rows) // 5
        
        if num_complete_bundles == 0:
            print("Not enough unprocessed items to create a complete bundle of 5.")
            return
        
        # Connect to the new bundle.db database to store the bundles
        bundle_conn = sqlite3.connect("bundle.db")
        bundle_cursor = bundle_conn.cursor()

        for i in range(num_complete_bundles):
            # Create a bundle from the next 5 items
            bundle = rows[i * 5:(i + 1) * 5]
            bundled_items = [item[1] for item in bundle]  # Assuming item[1] is the actual item
            items_str = ', '.join(bundled_items)
            print(f"Bundling items: {items_str}")

            # Insert the bundle into the new database
            bundle_cursor.execute('INSERT INTO bundled_items (items) VALUES (?)', (items_str,))
            bundle_conn.commit()

            # Mark these items as processed in the original database
            item_ids = [item[0] for item in bundle]  # Assuming item[0] is the ID
            cursor.execute(f"UPDATE {table_name} SET processed = 1 WHERE id IN ({', '.join('?' for _ in item_ids)})", item_ids)
            conn.commit()

        print(f"{num_complete_bundles} complete bundle(s) of unprocessed items added to 'bundle.db'.")
        
    except sqlite3.Error as e:
        print(f"Error reading from SQLite database: {e}")
    finally:
        # Close connections if they were opened
        if bundle_conn:
            bundle_conn.close()
        conn.close()

if __name__ == "__main__":
    database_path = "example.db"
    table_name = "items"

    # Ensure bundle.db has the necessary table
    create_bundle_table()

    # Process and bundle unprocessed items
    bundle_items(database_path, table_name)
