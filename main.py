import sys
import time
from database import Database
from apriori import Apriori
from bruteforce import BruteForce
from tabulate import tabulate

if __name__ == "__main__":
    TABLES = dict()
    execution_time = []
    apriori_execution_time = list()
    bruteforce_execution_time = list()

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

    # Read Minimum Support and Confidence values from command line
    try:
        min_support = float(sys.argv[1])
        min_confidence = float(sys.argv[2])

        if ((min_support <= 0 or min_confidence <= 0) or
                (min_support > 100 or min_confidence > 100)):
            print(f'Minimum Support and confidence should be between 1 and 100')
            exit(1)
    except Exception as e:
        print(f'Usage: python main.py <<minimum_support>> <<minimum_confidence>>')
        print(f'Note: Minimum Support and confidence should be an integer or a floating point value')
        exit(1)

    # Connect to the Database and Create items
    db = Database()
    db.connect_database()
    db.create_table(TABLES)
    db.insert_records()

    # Fetch the records from each database and run Apriori and Brute Force Algorithm
    records = db.fetch_records()

    for record in records:
        # Display Database Transactions
        transactions = records[record]
        heading = f'\n{record.upper()} Transactions\n'
        print(tabulate([[heading]], tablefmt="grid"))
        # List for tabulate display
        tabulate_list = []
        for trans_id, row in enumerate(transactions, 1):
            tabulate_list.append([trans_id, row])
        print(tabulate(tabulate_list, tablefmt="pretty", headers=["Transaction_ID", "Items"], stralign="left"))

        # Run Apriori Algorithm
        heading = f'\nCalculating Association rules using Apriori Algorithm\n'
        print(tabulate([[heading]], tablefmt="grid"))
        apriori = Apriori(transactions, min_support, min_confidence)
        # Start the timer
        start = time.perf_counter()
        apriori.execute_algorithm()
        # Stop the timer
        stop = time.perf_counter()
        apriori_execution_time.append(stop-start)

        # Run Brute Force Algorithm
        heading = f'\nCalculating Association rules using Brute Force Algorithm\n'
        print(tabulate([[heading]], tablefmt="grid"))
        bruteforce = BruteForce(transactions, min_support, min_confidence)
        # Start the timer
        start = time.perf_counter()
        bruteforce.execute_algorithm()
        # Stop the timer
        stop = time.perf_counter()
        bruteforce_execution_time.append(stop - start)

    # Close the DB connection
    db.close_connection()

    # Display the execution time comparison between the two algorithms
    print(tabulate([["Execution Time Comparison"]], tablefmt="grid"))
    execution_time = list(zip(TABLES.keys(), apriori_execution_time, bruteforce_execution_time))
    print(tabulate(execution_time, headers=["Database Used", "Apriori Algorithm",
                                            "Brute Force Algorithm"], tablefmt="fancy_grid"))
