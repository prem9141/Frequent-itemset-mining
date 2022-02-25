from itertools import combinations

class Apriori:
    def __init__(self, database, support):
        self.database = database
        self.total_transactions = len(self.database)
        self.candidate_item_set = list()
        self.frequent_item_set = list()
        self.not_frequent_item_set = list()
        self.min_support = support

    def scan_database(self):
        item_set = list()
        for record in self.database:
            for item in record:
                item_set.append(item)
        item_set = [{item} for item in set(item_set)]
        # print(item_set)
        return item_set

    def calculate_candidate_item_set(self, item_set):
        candidate_item_set = dict()
        for record in self.database:
            for item in item_set:
                # print(item, record)
                if item.issubset(record):
                    # print('hi')
                    candidate_item_set[frozenset(item)] = candidate_item_set.get(frozenset(item), 0) + 1

        # print(candidate_item_set)
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
        for subset in self.not_frequent_item_set[k-2]:
            if subset.issubset(superset):
                return True
        return False

    def perform_apriori_algorithm(self):
        k = 1
        unique_item_list = self.scan_database()
        self.calculate_candidate_item_set(unique_item_list)
        self.find_frequent_item_set(self.candidate_item_set[k-1])

        while len(self.frequent_item_set[k-1]) >= 2:
            new_item_set = set()
            for items in self.frequent_item_set[k-1]:
                for item in items:
                    new_item_set.add(item)

            k = k+1
            unique_item_list = list()
            for combination in combinations(new_item_set, k):
                new_combination_set = set(combination)
                if not self.is_subset_not_frequent(new_combination_set, k):
                    unique_item_list.append(new_combination_set)
            # print(unique_item_list)

            self.calculate_candidate_item_set(unique_item_list)
            self.find_frequent_item_set(self.candidate_item_set[k-1])

            # print("Frequent", apriori.frequent_item_set)
            # print("Not Frequent", apriori.not_frequent_item_set)
            # print("Candidate", apriori.candidate_item_set)

    def get_support(self, item_set):
        return self.frequent_item_set[len(item_set)-1][item_set]

    def generate_association_rule(self):
        for item_set in self.frequent_item_set[1:]:
            for items in item_set:
                for item in items:
                    right_side_set = frozenset([item])
                    left_side_set = items.difference(right_side_set)
                    # print(set(left_side_set), "==>", set(right_side_set))
                    # print(self.get_support(items))
                    # print(self.get_support(right_side_set))

                    if self.get_support(items)/self.get_support(left_side_set) >= 0.50:
                        print(set(left_side_set), "==>", set(right_side_set))

            #print(items)


if __name__ == "__main__":
    # data = [set(['ink', 'pen', 'cheese', 'bag']), set(['milk', 'pen', 'juice', 'cheese']), set(['milk', 'juice']),
    #         set(['juice', 'milk', 'cheese'])]
    data = [set(['X', 'Y', 'Z']), set(['X', 'Z']), set(['X', 'W']), set(['M', 'Y', 'N'])]
    min_support = 50
    apriori = Apriori(data, min_support)
    apriori.perform_apriori_algorithm()
    apriori.generate_association_rule()


