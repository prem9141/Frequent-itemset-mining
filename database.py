import mysql.connector as mysql
from mysql.connector import errorcode


class Database:
    def __init__(self, connect_params):
        try:
            self.cnx = mysql.connect(**connect_params)
            self.cursor = self.cnx.cursor()
        except mysql.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def create_database(self, db_name):
        try:
            self.cursor.execute(f"CREATE DATABASE {db_name} DEFAULT CHARACTER SET 'utf8mb4'")
        except mysql.Error as err:
            print(f"Failed creating database {db_name}: {err}")
            exit(1)

    def connect_database(self, db_name):
        try:
            self.cursor.execute(f'USE {db_name}')
        except mysql.Error as err:
            print(f'{db_name} does not exists')
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print(f'Creating database {db_name}')
                self.create_database(db_name)
                self.cnx.dataset = db_name
            else:
                print(err)
                exit(1)

    def create_table(self, tables):
        try:
            for table in tables:
                self.cursor.execute(tables[table])
        except mysql.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)

    def insert_records(self):
        try:
            add_insert = "INSERT INTO DATASET_1 (TRANS_ID, ITEMS) VALUES (%s, %s)"
            add_values = [(1, "Water, Cocoa, Cider"),
              (2, "Cocoa, Water, Juice"),
              (3, "Cocktail"),
              (4, "Tea, Cocktail, Wine, Coffee, Water"),
              (5, "Cocktail, Juice, ProteinShake, Soda"),
              (6, "Tea, ProteinShake, Coffee, Soda"),
              (7, "Water"),
              (8, "Water, Cocoa, Wine"),
              (9, "Juice, Cocoa, Water, Coffee, Tea, Cider"),
              (10, "Cocoa, Tea, Water, Coffee, Wine"),
              (11, "Soda, Tea, Coffee, ProteinShake, Juice"),
              (12, "Cocoa, Cocktail, Juice, ProteinShake, Water"),
              (13, "Coffee, Tea, ProteinShake, Cocktail, Water, Cider"),
              (14, "Cocktail, Coffee, ProteinShake, Wine, Juice"),
              (15, "Soda, Coffee, Cider"),
              (16, "ProteinShake, Water, Coffee"),
              (17, "ProteinShake, Cocktail, Ciderss"),
              (18, "Coffee, Cocktail, Cocoa, Wine, ProteinShake, Water"),
              (19, "Juice, Coffee, Soda"),
              (20, "Soda")
              ]

            self.cursor.executemany(add_insert, add_values)
            self.cnx.commit()
        except mysql.Error as err:
            print(err)
            exit(1)

    def fetch_records(self):
        items_list = list()
        try:
            self.cursor.execute("SELECT ITEMS FROM DATASET_1")
            for items in self.cursor:
                for item in items:
                    list_split = item.split(", ")
                    items_list.append(set(list_split))
            return items_list
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


if __name__ == '__main__':
    DB_NAME = 'cs634_data_mining_project'

    config = {
        'user': 'root',
        'password': 'Maharaj3n$$$567',
        'host': '127.0.0.1',
        'raise_on_warnings': True
    }

    TABLES = dict()
    TABLES['dataset_1'] = (
        "CREATE TABLE `dataset_1` ("
        "  `trans_id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `items` varchar(255) NOT NULL,"
        "  PRIMARY KEY (`trans_id`)"
        ") ENGINE=InnoDB")

    db = Database(config)
    db.connect_database(DB_NAME)
    # db.create_table(TABLES)
    # db.insert_records()
    db.fetch_records()
    db.close_connection()
