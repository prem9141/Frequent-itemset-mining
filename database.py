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
        """
        Creates the database
        """
        try:
            self.cursor.execute(f"CREATE DATABASE {self.dbname} DEFAULT CHARACTER SET 'utf8mb4'")
        except mysql.Error as err:
            print(f"Failed creating database {self.dbname}: {err}")
            exit(1)

    def connect_database(self):
        """
        Connects to the database if it exists else creates the database and connects to it
        """
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
        """
        Creates the specified table in the database
        :param dict tables: Tables to be created in the database. Dict keys contains the table name and value holds the
         sql query
        """
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
        """
        Reads the data from the file
        :param str fname: File from which data has to be read
        :return: File Contents
        :rtype: list
        """
        fname = "./" + fname + ".txt"
        records = list()
        with open(fname, 'r') as file:
            for line in file.readlines():
                line = line.strip()
                trans_id, items = line.split(' ', 1)
                records.append((int(trans_id), items))
        return records

    def insert_records(self):
        """
        Inserts record into the table
        """
        try:
            for table in self.tables:
                add_insert = f"INSERT INTO {table} (TRANS_ID, ITEMS) VALUES (%s, %s)"
                add_values = self.fetch_file_data(table)
                self.cursor.executemany(add_insert, add_values)
                self.cnx.commit()
        except mysql.Error as err:
            print(err)
            exit(1)

    def fetch_records(self, table):
        """
        Returns the table contents
        :rtype: dict
        """
        table_records = dict()
        try:
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
        """
        Closes the Cursor and Connection objects
        """
        try:
            self.cnx.close()
            self.cursor.close()
        except mysql.Error as err:
            print(err)
            exit(1)


if __name__ == "__main__":
    TABLES = dict()

    # Table Structure
    TABLES['database1'] = (
        "CREATE TABLE `database1` ("
        "  `trans_id` int NOT NULL AUTO_INCREMENT,"
        "  `items` varchar(255) NOT NULL,"
        "  PRIMARY KEY (`trans_id`)"
        ") ENGINE=InnoDB")

    TABLES['database2'] = (
        "CREATE TABLE `database2` ("
        "  `trans_id` int NOT NULL AUTO_INCREMENT,"
        "  `items` varchar(255) NOT NULL,"
        "  PRIMARY KEY (`trans_id`)"
        ") ENGINE=InnoDB")

    TABLES['database3'] = (
        "CREATE TABLE `database3` ("
        "  `trans_id` int NOT NULL AUTO_INCREMENT,"
        "  `items` varchar(255) NOT NULL,"
        "  PRIMARY KEY (`trans_id`)"
        ") ENGINE=InnoDB")

    TABLES['database4'] = (
        "CREATE TABLE `database4` ("
        "  `trans_id` int NOT NULL AUTO_INCREMENT,"
        "  `items` varchar(255) NOT NULL,"
        "  PRIMARY KEY (`trans_id`)"
        ") ENGINE=InnoDB")

    TABLES['database5'] = (
        "CREATE TABLE `database5` ("
        "  `trans_id` int NOT NULL AUTO_INCREMENT,"
        "  `items` varchar(255) NOT NULL,"
        "  PRIMARY KEY (`trans_id`)"
        ") ENGINE=InnoDB")

    db = Database()
    db.connect_database()
    db.create_table(TABLES)
    db.insert_records()