import time
from collections import defaultdict
from itertools import combinations
import psutil
import os


class Itemset:
    def __init__(self, items):
        self.itemset = items
        self.support = 0

    def __str__(self):
        return "{" + ", ".join(map(str, self.itemset)) + "}"


class Itemsets:
    def __init__(self, name):
        self.name = name
        self.itemsets = {}

    def add_itemset(self, itemset, size):
        if size not in self.itemsets:
            self.itemsets[size] = []
        self.itemsets[size].append(itemset)


class ArraysAlgos:
    @staticmethod
    def same_as(arr1, arr2, pos_removed):
        len1, len2 = len(arr1), len(arr2)

        for i in range(min(len1, len2)):
            if i == pos_removed:
                continue

            if arr1[i] < arr2[i]:
                return -1
            elif arr1[i] > arr2[i]:
                return 1

        if len1 < len2:
            return -1
        elif len1 > len2:
            return 1
        else:
            return 0


class MemoryLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemoryLogger, cls).__new__(cls)
            cls._instance.memory_used = 0
        return cls._instance

    @staticmethod
    def get_instance():
        if MemoryLogger._instance is None:
            MemoryLogger._instance = MemoryLogger()
        return MemoryLogger._instance

    def check_memory(self):
        self.memory_used = psutil.Process(os.getpid()).memory_info().rss

    def reset(self):
        self.memory_used = 0


class AlgoApriori:
    def __init__(self):
        self.k = 0
        self.total_candidate_count = 0
        self.start_timestamp = 0
        self.end_timestamp = 0
        self.itemset_count = 0
        self.database_size = 0
        self.minsup_relative = 0
        self.database = None
        self.patterns = None
        self.writer = None
        self.max_pattern_length = 4

    def run_algorithm(self, minsup, input_file):
        self.patterns = Itemsets("FREQUENT ITEMSETS")

        self.start_timestamp = int(round(time.time() * 1000))
        self.itemset_count = 0
        self.total_candidate_count = 0
        MemoryLogger.get_instance().reset()

        database = []
        map_item_count = {}

        with open(input_file, "r") as reader:
            for line in reader:
                if line.strip() == "" or line[0] in ['#', '%', '@']:
                    continue

                line_splitted = line.split()
                transaction = [int(item) for item in line_splitted]

                for item in transaction:
                    if item in map_item_count:
                        map_item_count[item] += 1
                    else:
                        map_item_count[item] = 1

                database.append(transaction)
                self.database_size += 1

        self.minsup_relative = int(minsup * self.database_size)
        self.k = 1

        frequent1 = [item for item, count in map_item_count.items() if count >= self.minsup_relative]
        frequent1.sort()

        if not frequent1 or self.max_pattern_length <= 1:
            self.end_timestamp = int(round(time.time() * 1000))
            MemoryLogger.get_instance().check_memory()

            return self.patterns

        self.total_candidate_count += len(frequent1)

        level = None
        self.k = 2
        while True:
            MemoryLogger.get_instance().check_memory()

            if self.k == 2:
                candidates_k = self.generate_candidate_2(frequent1)
            else:
                candidates_k = self.generate_candidate_size_k(level)

            self.total_candidate_count += len(candidates_k)

            for transaction in database:
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
            if self.k < self.max_pattern_length + 1:
                for candidate in candidates_k:
                    if candidate.support >= self.minsup_relative:
                        level.append(candidate)
                        self.save_itemset(candidate)
                        

            if not level:
                break

            self.k += 1

        self.end_timestamp = int(round(time.time() * 1000))
        MemoryLogger.get_instance().check_memory()

        return self.patterns

    def generate_candidate_2(self, frequent_1):
        candidates = []

        for i in range(len(frequent_1)):
            for j in range(i + 1, len(frequent_1)):
                candidates.append(Itemset([frequent_1[i], frequent_1[j]]))

        return candidates

    def generate_candidate_size_k(self, level):
        candidates = []

        for i in range(len(level)):
            for j in range(i + 1, len(level)):
                itemset1 = level[i].itemset
                itemset2 = level[j].itemset

                if ArraysAlgos.same_as(itemset1, itemset2, -1) == 0:
                    candidate = Itemset(itemset1 + [itemset2[-1]])
                    if self.is_candidate_frequent(candidate, level):
                        candidates.append(candidate)
                        self.total_candidate_count += 1
                else:
                    break

        return candidates

    def is_candidate_frequent(self, candidate, level):
        subsets = list(combinations(candidate.itemset, self.k - 1))

        for subset in subsets:
            subset_itemset = Itemset(list(subset))
            if not self.is_itemset_in_list(subset_itemset, level):
                return False

        return True

    def is_itemset_in_list(self, itemset, level):
        for i in range(len(level)):
            if ArraysAlgos.same_as(itemset.itemset, level[i].itemset, -1) == 0:
                return True

        return False

    def save_itemset(self, candidate):
        if candidate.support >= self.minsup_relative:
            self.patterns.add_itemset(candidate, self.k)
            self.itemset_count += 1


if __name__ == "__main__":
    apriori = AlgoApriori()
    minsup = 0.4  # Adjust the minimum support threshold as needed
    input_file = "your_input_file.txt"  # Provide the path to your input file

    result = apriori.run_algorithm(minsup, input_file)

    print("============= APRIORI - STATS =============")
    print(f"Candidates count : {apriori.total_candidate_count}")
    print(f"The algorithm stopped at size {apriori.k - 1}")
    print(f"Frequent itemsets count : {apriori.itemset_count}")
    print(f"Maximum memory usage : {MemoryLogger.get_instance().memory_used / (1024 * 1024):.6f} mb")
    print(f"Total time ~ {apriori.end_timestamp - apriori.start_timestamp} ms")
    print("===========================================")

    if result is not None:
        print("\n ------- FREQUENT ITEMSETS -------")
        max_level = max(result.itemsets.keys(), default=0)
        for level in range(max_level + 1):
            level_label = f"L{level}"
            print(f"  {level_label}")
            if level in result.itemsets:
                for i, itemset in enumerate(result.itemsets[level]):
                    print(f"  pattern {i}:  {', '.join(map(str, itemset.itemset))} support : {itemset.support}")
            else:
                print("  (empty)")
    print(" ---------------------------------")

