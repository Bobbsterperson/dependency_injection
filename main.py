from item_manager import main as bundler_main
from sqlite_manage import SQLiteConnector

def run_bundler():
    bundler_main()

def add_items():
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

def main():
    add_items()
    run_bundler()

if __name__ == "__main__":
    main()
