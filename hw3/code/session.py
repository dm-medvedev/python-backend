import csv
import sqlite3
from typing import List


class Session():
    def __init__(self):
        self.connection = sqlite3.connect(":memory:")

    def create_table(self, table_name: str, columns: List[str]):
        self.connection.execute(f"CREATE TABLE {table_name}"
                                f" ({', '.join(columns)});")
        self.connection.commit()

    def table_from_csv(self, table_name: str, data_path: str,
                       column_types=None):
        with open(data_path, 'r') as table:
            csvl = list(csv.DictReader(table,
                        fieldnames=['city', 'region'], delimiter=';'))
            columns = list(csvl.pop(0).keys())
            if column_types is None:
                to_db = [tuple(d[c] for c in columns) for d in csvl]
            else:
                to_db = [tuple(column_types[c](d[c])
                               for c in columns) for d in csvl]
        self.create_table(table_name, columns)
        command = f"INSERT INTO {table_name} " + \
                  f"({', '.join(columns)}) " + \
                  f"VALUES ({', '.join('?'*len(columns))});"
        self.connection.executemany(command, to_db)
        self.connection.commit()

    def table_exists(self, table_name: str):
        command = "SELECT name FROM sqlite_master WHERE" + \
                  " type='table' AND name=?;"
        cur = self.connection.execute(command, (table_name,))
        return len(list(cur)) != 0
