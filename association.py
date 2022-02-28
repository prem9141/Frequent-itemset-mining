from tabulate import tabulate


class Association:
    def __init__(self, data, support, confidence):
        self.dataset = data
        self.total_transactions = len(self.dataset)
        self.candidate_item_set = list()
        self.frequent_item_set = list()
        self.not_frequent_item_set = list()
        self.min_support = support
        self.min_confidence = confidence
        self.selected_association_rule = list()
        self.rejected_association_rule = list()

    def scan_database(self):
        item_set = list()
        for record in self.dataset:
            for item in record:
                item_set.append(item)

        item_set = [{item} for item in set(item_set)]

        return item_set

    def generate_candidate_item_set(self, item_set):
        candidate_item_set = dict()
        for record in self.dataset:
            for item in item_set:
                if item.issubset(record):
                    candidate_item_set[frozenset(item)] = candidate_item_set.get(frozenset(item), 0) + 1

        for key in candidate_item_set.keys():
            candidate_item_set[key] = candidate_item_set.get(key) / self.total_transactions * 100

        self.candidate_item_set.append(candidate_item_set)

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

    def check_if_subset_not_frequent(self, superset, k):
        for subset in self.not_frequent_item_set[k - 2]:
            if subset.issubset(superset):
                return True
        return False

    def get_support(self, item_set):
        return self.frequent_item_set[len(item_set) - 1][item_set]

    def generate_association_rule(self):
        for item_set in self.frequent_item_set[1:]:
            for items in item_set:
                for item in items:
                    right_side_set = frozenset([item])
                    left_side_set = items.difference(right_side_set)

                    item_support = self.get_support(items)
                    confidence = item_support / self.get_support(left_side_set) * 100

                    if confidence >= self.min_confidence:
                        self.selected_association_rule.append(
                            [set(left_side_set), set(right_side_set), f'{item_support:.2f}%', f'{confidence:.2f}%'])
                    else:
                        self.rejected_association_rule.append(
                            [set(left_side_set), set(right_side_set), f'{item_support:.2f}%', f'{confidence:.2f}%'])

    def display_results(self):
        for i in range(len(self.candidate_item_set)):
            heading = f'\nCandidate {i+1}-Itemsets\n'
            print(tabulate([[heading]], tablefmt="rst"))
            candidate_tabulate_list = []
            for item in self.candidate_item_set[i]:
                candidate_tabulate_list.append([set(item), f'{self.candidate_item_set[i][item]:.2f}%'])
            print(tabulate(candidate_tabulate_list, tablefmt="pretty", headers=["Itemset", "Support"], stralign="left"))

            heading = f'\nFrequent {i + 1}-Itemsets\n'
            print(tabulate([[heading]], tablefmt="rst"))
            frequent_tabulate_list = []
            if len(self.frequent_item_set[i]) >= 1:
                for item in self.frequent_item_set[i]:
                    frequent_tabulate_list.append([set(item), f'{self.frequent_item_set[i][item]:.2f}%'])
                print(tabulate(frequent_tabulate_list, tablefmt="pretty",
                               headers=["Itemset", "Support"], stralign="left"))
            else:
                print("None")

            heading = f'\nNot Frequent {i + 1}-Itemsets\n'
            print(tabulate([[heading]], tablefmt="rst"))
            not_frequent_tabulate_list = []
            if len(self.not_frequent_item_set[i]) >= 1:
                for item in self.not_frequent_item_set[i]:
                    not_frequent_tabulate_list.append([set(item), f'{self.not_frequent_item_set[i][item]:.2f}%'])
                print(tabulate(not_frequent_tabulate_list, tablefmt="pretty",
                               headers=["Itemset", "Support"], stralign="left"))
            else:
                print("None")

        heading = f'\nRejected Association Rules\n'
        print(tabulate([[heading]], tablefmt="grid"))
        if len(self.rejected_association_rule) >= 1:
            print(tabulate(self.rejected_association_rule, tablefmt="fancy_grid",
                  headers=["Antecedent", "Consequent", "Support", "Confidence"]))
        else:
            print("None")

        heading = f'\nAccepted Association Rules\n'
        print(tabulate([[heading]], tablefmt="grid"))
        if len(self.selected_association_rule) >= 1:
            print(tabulate(self.selected_association_rule, tablefmt="fancy_grid",
                  headers=["Antecedent", "Consequent", "Support", "Confidence"]))
        else:
            print("None")
