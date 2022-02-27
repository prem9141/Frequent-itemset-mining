from association import Association
from itertools import combinations


class Apriori(Association):
    def __init__(self, data, support, confidence):
        super().__init__(data, support, confidence)

    def execute_algorithm(self):
        k = 1
        unique_item_list = self.scan_database()
        self.generate_candidate_item_set(unique_item_list)
        self.find_frequent_item_set(self.candidate_item_set[k - 1])

        while len(self.frequent_item_set[k - 1]) >= 2:
            new_item_set = set()
            for items in self.frequent_item_set[k - 1]:
                for item in items:
                    new_item_set.add(item)

            k = k + 1
            unique_item_list = list()
            for combination in combinations(new_item_set, k):
                new_combination_set = set(combination)
                if not self.check_if_subset_not_frequent(new_combination_set, k):
                    unique_item_list.append(new_combination_set)

            self.generate_candidate_item_set(unique_item_list)
            self.find_frequent_item_set(self.candidate_item_set[k - 1])

        self.generate_association_rule()
        self.display_results()
