from itertools import combinations
import database


class BruteForce:
    def __init__(self, data, support, confidence):
        self.dataset = data
        self.total_transactions = len(self.dataset)
        self.candidate_item_set = list()
        self.frequent_item_set = list()
        self.not_frequent_item_set = list()
        self.min_support = support
        self.min_confidence = confidence

    def scan_database(self):
        item_set = list()
        for record in self.dataset:
            for item in record:
                item_set.append(item)
        # print(item_set)
        item_set = [{item} for item in set(item_set)]
        # print(len(item_set))
        return item_set

    def calculate_candidate_item_set(self, item_set):
        candidate_item_set = dict()
        for record in self.dataset:
            for item in item_set:
                # print("Item:", item, "Record:", record)
                if item.issubset(record):
                    candidate_item_set[frozenset(item)] = candidate_item_set.get(frozenset(item), 0) + 1
                    # print("Candidate Item:", candidate_item_set)

        for key in candidate_item_set.keys():
            candidate_item_set[key] = candidate_item_set.get(key) / self.total_transactions * 100

        # print(candidate_item_set)
        self.candidate_item_set.append(candidate_item_set)
        # print(self.candidate_item_set)

    def find_frequent_item_set(self, item_set):
        frequent_item_set = dict()
        not_frequent_item_set = dict()

        for item in item_set.keys():
            if item_set[item] >= self.min_support:
                frequent_item_set[item] = item_set[item]
            else:
                not_frequent_item_set[item] = item_set[item]

        self.frequent_item_set.append(frequent_item_set)
        self.not_frequent_item_set.append(not_frequent_item_set)

    def is_subset_not_frequent(self, superset, k):
        for subset in self.not_frequent_item_set[k - 2]:
            if subset.issubset(superset):
                return True
        return False

    def perform_bruteforce_algorithm(self):
        k = 1
        unique_item_list = self.scan_database()
        self.calculate_candidate_item_set(unique_item_list)
        self.find_frequent_item_set(self.candidate_item_set[k - 1])
        # print("Unique", unique_item_list)
        # print("Candidate", self.candidate_item_set)
        # print("Frequent", self.frequent_item_set)

        unique_item_list = [items.pop() for items in unique_item_list]
        # print("Unique", unique_item_list)

        while len(self.frequent_item_set[k - 1]) >= 1:
            # new_item_set = set()
            # for items in self.candidate_item_set[k - 1]:
            #     for item in items:
            #         new_item_set.add(item)

            k = k + 1
            new_item_list = list()
            for combination in combinations(unique_item_list, k):
                # print(combination)
                new_combination_set = set(combination)
                new_item_list.append(new_combination_set)

            # print(new_item_list)

            self.calculate_candidate_item_set(new_item_list)
            self.find_frequent_item_set(self.candidate_item_set[k - 1])

            # print("Candidate", apriori.candidate_item_set)
            # print("Frequent", apriori.frequent_item_set)
            # print("Not Frequent", apriori.not_frequent_item_set)

    def get_support(self, item_set):
        return self.frequent_item_set[len(item_set) - 1][item_set]

    def generate_association_rule(self):
        # print(self.min_confidence)
        for item_set in self.frequent_item_set[1:]:
            for items in item_set:
                for item in items:
                    right_side_set = frozenset([item])
                    left_side_set = items.difference(right_side_set)
                    # print(set(left_side_set), "==>", set(right_side_set))
                    # print(self.get_support(items))
                    # print(self.get_support(left_side_set))

                    confidence = self.get_support(items) / self.get_support(left_side_set) * 100

                    # print(confidence)

                    if confidence >= self.min_confidence:
                        print(set(left_side_set), "==>", set(right_side_set), confidence)

            # print(items)


if __name__ == "__main__":
    # data = [set(['ink', 'pen', 'cheese', 'bag']), set(['milk', 'pen', 'juice', 'cheese']), set(['milk', 'juice']),
    #         set(['juice', 'milk', 'cheese'])]
    # print(data)

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

    db = database.Database(config)
    db.connect_database(DB_NAME)
    # db.create_table(TABLES)
    # db.insert_records()
    min_support = 20
    min_confidence = 40
    bruteforce = BruteForce(db.fetch_records(), min_support, min_confidence)
    # apriori = Apriori(data, min_support, min_confidence)
    bruteforce.perform_bruteforce_algorithm()
    bruteforce.generate_association_rule()
    db.close_connection()
