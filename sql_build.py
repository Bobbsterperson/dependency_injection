class SQLBuilder:
    def __init__(self):
        self.query = ""
        self.params = []

    def select(self, columns, table, condition=None):
        self.query = f"SELECT {columns} FROM {table}"
        if condition:
            self.query += f" WHERE {condition}"
        return self

    def insert(self, table, columns):
        placeholders = ', '.join('?' for _ in columns)
        self.query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        return self

    def update(self, table, set_clause, condition):
        self.query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        return self

    def values(self, *args):
        self.params.extend(args)
        return self

    def build(self):
        return self.query, self.params
