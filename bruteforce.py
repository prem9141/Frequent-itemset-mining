from itertools import combinations
from association import Association


class BruteForce(Association):
    def __init__(self, data, support, confidence):
        super().__init__(data, support, confidence)

    def execute_algorithm(self):
        k = 1
        unique_item_list = self.scan_database()
        self.generate_candidate_item_set(unique_item_list)
        self.find_frequent_item_set(self.candidate_item_set[k - 1])

        unique_item_list = [items.pop() for items in unique_item_list]

        while len(self.frequent_item_set[k - 1]) >= 1:
            k = k + 1
            new_item_list = list()
            for combination in combinations(unique_item_list, k):
                new_combination_set = set(combination)
                new_item_list.append(new_combination_set)

            self.generate_candidate_item_set(new_item_list)
            self.find_frequent_item_set(self.candidate_item_set[k - 1])

        self.generate_association_rule()
        self.display_results()