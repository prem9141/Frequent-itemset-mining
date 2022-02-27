import mysql.connector as mysql
from mysql.connector import errorcode

DB_NAME = 'cs634_data_mining_project'

config = {
    'user': 'root',
    'password': 'Maharaj3n$$$567',
    'host': '127.0.0.1',
    'raise_on_warnings': True
}


class Database:
    def __init__(self):
        try:
            self.cnx = mysql.connect(**config)
            self.cursor = self.cnx.cursor()
            self.dbname = DB_NAME
            self.tables = None
        except mysql.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def create_database(self):
        try:
            self.cursor.execute(f"CREATE DATABASE {self.dbname} DEFAULT CHARACTER SET 'utf8mb4'")
        except mysql.Error as err:
            print(f"Failed creating database {self.dbname}: {err}")
            exit(1)

    def connect_database(self):
        try:
            self.cursor.execute(f'USE {self.dbname}')
        except mysql.Error as err:
            print(f'{self.dbname} does not exists')
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print(f'Creating database {self.dbname}')
                self.create_database(self.dbname)
                self.cnx.dataset = self.dbname
            else:
                print(err)
                exit(1)

    def create_table(self, tables):
        self.tables = tables;
        try:
            for table in self.tables.keys():
                self.cursor.execute(self.tables[table])
        except mysql.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)

    def fetch_file_data(self, fname):
        fname = "./" + fname + ".txt"
        records = list()
        with open(fname, 'r') as file:
            for line in file.readlines():
                line = line.strip()
                trans_id, items = line.split(' ', 1)
                records.append((int(trans_id), items))
        return records

    def insert_records(self):
        try:
            for table in self.tables:
                add_insert = f"INSERT INTO {table} (TRANS_ID, ITEMS) VALUES (%s, %s)"
                add_values = self.fetch_file_data(table)
                self.cursor.executemany(add_insert, add_values)
                self.cnx.commit()
        except mysql.Error as err:
            print(err)
            exit(1)

    def fetch_records(self):
        table_records = dict()
        try:
            for table in self.tables:
                self.cursor.execute(f"SELECT ITEMS FROM {table}")
                items_list = list()
                for items in self.cursor:
                    for item in items:
                        list_split = item.split(", ")
                        items_list.append(set(list_split))
                table_records[table] = items_list
            return table_records
        except mysql.Error as err:
            print(err)
            exit(1)

    def close_connection(self):
        try:
            self.cnx.close()
            self.cursor.close()
        except mysql.Error as err:
            print(err)
            exit(1)
