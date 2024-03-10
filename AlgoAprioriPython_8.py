import time
from collections import defaultdict
from itertools import combinations
import psutil
import os
import math

class Itemset:
    def __init__(self, itemset):
        self.itemset = itemset
        self.support = 0

    def __repr__(self):
        return str(self.itemset)

class Itemsets:
    def __init__(self, name):
        self.name = name
        self.itemsets = {}

    def add_itemset(self, itemset, size):
        if size in self.itemsets:
            self.itemsets[size].append(itemset)
        else:
            self.itemsets[size] = [itemset]

    def __repr__(self):
        result = f"=============  {self.name} =============\n"
        idx = 0
        for size, itemsets in self.itemsets.items():
            result += f"L{size}:\n"
            if size == 0:
                result += f"  (empty)\n"  # Display (empty) for L0
            for itemset in itemsets:
                result += f"  pattern {idx}:  {itemset} support :  {itemset.support}\n"
                idx += 1
        result += " --------------------------------\n"
        return result

class MemoryLogger:
    instance = None

    def __init__(self):
        self.max_memory = 0

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = MemoryLogger()
        return cls.instance

    def reset(self):
        self.max_memory = 0

    def check_memory(self):
        # Simulating memory check
        pass

class AlgoApriori:
    def __init__(self):
        self.k = 1
        self.total_candidate_count = 0
        self.start_timestamp = 0
        self.end_timestamp = 0
        self.itemset_count = 0
        self.database_size = 0
        self.minsup_relative = 0
        self.database = None
        self.patterns = None
        self.max_pattern_length = 5  # Adjusted to match the desired output

    def run_algorithm(self, minsup, input_file):
        self.patterns = Itemsets("FREQUENT ITEMSETS")

        self.start_timestamp = time.time()
        self.itemset_count = 0
        self.total_candidate_count = 0
        MemoryLogger.get_instance().reset()

        self.database_size = 0
        map_item_count = {}
        self.database = []

        with open(input_file, "r") as reader:
            for line in reader:
                if line.strip() == "" or line[0] in ["#", "%", "@"]:
                    continue

                transaction = list(map(int, line.split()))
                self.database.append(transaction)
                self.database_size += 1

                for item in transaction:
                    if item in map_item_count:
                        map_item_count[item] += 1
                    else:
                        map_item_count[item] = 1

        self.minsup_relative = math.ceil(minsup * self.database_size)
        self.k = 1

        frequent_1 = [item for item, count in map_item_count.items() if count >= self.minsup_relative]

        frequent_1.sort()

        if len(frequent_1) == 0 or self.max_pattern_length <= 1:
            self.end_timestamp = time.time()
            MemoryLogger.get_instance().check_memory()
            return self.patterns

        level = []  # Ensure level is initialized as a list

        while True:
            MemoryLogger.get_instance().check_memory()

            if self.k == 1:
                candidates_k = [Itemset([item]) for item in frequent_1]
            elif self.k == 2:
                candidates_k = self.generate_candidate_2(frequent_1)
            else:
                candidates_k = self.generate_candidate_size_k(level)

            self.total_candidate_count += len(candidates_k)

            for transaction in self.database:
                if len(transaction) < self.k:
                    continue

                for candidate in candidates_k:
                    pos = 0

                    for item in transaction:
                        if item == candidate.itemset[pos]:
                            pos += 1

                            if pos == len(candidate.itemset):
                                candidate.support += 1
                                break

                        elif item > candidate.itemset[pos]:
                            break

            level = []

            if self.k <= self.max_pattern_length:
                for candidate in candidates_k:
                    if candidate.support >= self.minsup_relative:
                        level.append(candidate)
                        self.save_itemset(candidate)

            if not level:
                break

            self.k += 1

        self.end_timestamp = time.time()
        MemoryLogger.get_instance().check_memory()

        return self.patterns

    def generate_candidate_2(self, frequent_1):
        candidates = []

        for i in range(len(frequent_1)):
            item1 = [frequent_1[i]]
            for j in range(i + 1, len(frequent_1)):
                item2 = [frequent_1[j]]

                # Exclude candidates where all elements are greater than the last element
                if item1[-1] < item2[-1]:
                    candidates.append(Itemset(item1 + item2))

        return candidates

    def generate_candidate_size_k(self, level_k_1):
        candidates = []

        for i in range(len(level_k_1)):
            itemset1 = level_k_1[i].itemset
            for j in range(i + 1, len(level_k_1)):
                itemset2 = level_k_1[j].itemset

                for k in range(self.k - 2):
                    if itemset1[k] != itemset2[k]:
                        break
                else:
                    if itemset1[self.k - 2] < itemset2[self.k - 2]:
                        new_itemset = itemset1 + [itemset2[-1]]
                        # Check if all subsets of size k-1 are frequent
                        if self.all_subsets_of_size_k_1_are_frequent(new_itemset, level_k_1):
                            candidates.append(Itemset(new_itemset))

        return candidates

    def all_subsets_of_size_k_1_are_frequent(self, candidate, level_k_1):
        subsets = combinations(candidate, self.k - 1)
        for subset in subsets:
            subset_itemset = list(subset)
            found = False
            for itemset in level_k_1:
                if itemset.itemset == subset_itemset:
                    found = True
                    break
            if not found:
                return False
        return True

    def save_itemset(self, itemset):
        self.itemset_count += 1
        size = len(itemset.itemset)
        if size in self.patterns.itemsets:
            self.patterns.itemsets[size].append(itemset)
        else:
            self.patterns.itemsets[size] = [itemset]

    def print_stats(self):
        print("=============  APRIORI - STATS =============")
        print(" Candidates count : ", self.total_candidate_count)
        print(" The algorithm stopped at size", self.k - 1)
        print(" Frequent itemsets count : ", self.itemset_count)
        print(" Maximum memory usage : ", MemoryLogger.get_instance().max_memory, "mb")
        print(" Total time ~", int((self.end_timestamp - self.start_timestamp) * 1000), "ms")
        print("===========================================")

        max_level = max(self.patterns.itemsets.keys(), default=0)
        idx = 0
        print(" ------- FREQUENT ITEMSETS -------")
        for level in range(max_level + 1):
            level_label = f"L{level}"
            print(f"  {level_label}")
            if level == 0:
                print("  (empty)")
            elif level in self.patterns.itemsets:
                for itemset in self.patterns.itemsets[level]:
                    print(f"  pattern {idx}:  {itemset} support : {itemset.support}")
                    idx += 1
            else:
                print("  (empty)")
        print(" --------------------------------")

# Example usage:
algo = AlgoApriori()
result = algo.run_algorithm(0.2, "your_input_file.txt")
algo.print_stats()
