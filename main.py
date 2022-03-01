import sys
import time
from database import Database
from apriori import Apriori
from bruteforce import BruteForce
from tabulate import tabulate

if __name__ == "__main__":

    # Read Minimum Support and Confidence values from command line
    try:
        min_support = float(sys.argv[2])
        min_confidence = float(sys.argv[3])
        table_name = sys.argv[1]

        if ((min_support <= 0 or min_confidence <= 0) or
                (min_support > 100 or min_confidence > 100)):
            print(f'Minimum Support and confidence should be between 1 and 100')
            exit(1)
    except Exception as e:
        print(f'Usage: python main.py <<minimum_support>> <<minimum_confidence>>')
        print(f'Note: Minimum Support and confidence should be an integer or a floating point value')
        exit(1)

    # Connect to the Database and fetch records
    db = Database()
    db.connect_database()
    records = db.fetch_records(table_name)

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
        apriori_execution_time = stop-start

        # Run Brute Force Algorithm
        heading = f'\nCalculating Association rules using Brute Force Algorithm\n'
        print(tabulate([[heading]], tablefmt="grid"))
        bruteforce = BruteForce(transactions, min_support, min_confidence)
        # Start the timer
        start = time.perf_counter()
        bruteforce.execute_algorithm()
        # Stop the timer
        stop = time.perf_counter()
        bruteforce_execution_time = stop - start

    # Close the DB connection
    db.close_connection()

    # Display the execution time comparison between the two algorithms
    print(tabulate([["Execution Time Comparison"]], tablefmt="grid"))
    print(tabulate([[table_name.upper(), apriori_execution_time, bruteforce_execution_time]],
                   headers=["Database Used", "Apriori Algorithm (Seconds)",
                            "Brute Force Algorithm (Seconds)"], tablefmt="fancy_grid"))
