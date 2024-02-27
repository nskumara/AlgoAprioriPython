import time
from typing import List, Tuple

class Itemset:
    def __init__(self, itemset):
        self.itemset = itemset
        self.support = 0

    def size(self):
        return len(self.itemset)

    def get_absolute_support(self):
        return self.support

    def __str__(self):
        return " ".join(map(str, self.itemset))

class Itemsets:
    def __init__(self, name):
        self.name = name
        self.itemsets = {}

    def addItemset(self, itemset, size):
        self.itemsets.setdefault(size, []).append(itemset)

class MemoryLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemoryLogger, cls).__new__(cls)
            cls._instance.maxMemory = 0
        return cls._instance

    def reset(self):
        self.maxMemory = 0

    def checkMemory(self):
        currentMemory = (process.memory_info().rss) / 1024 / 1024
        if currentMemory > self.maxMemory:
            self.maxMemory = currentMemory
        return currentMemory

class ArraysAlgos:
    @staticmethod
    def sameAs(arr1, arr2, pos_removed):
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

class AlgoApriori:
    def __init__(self):
        self.k = 0
        self.totalCandidateCount = 0
        self.startTimestamp = 0
        self.endTimestamp = 0
        self.itemsetCount = 0
        self.databaseSize = 0
        self.minsupRelative = 0
        self.database = None
        self.patterns = None
        self.writer = None
        self.maxPatternLength = 10000

    def runAlgorithm(self, minsup, input_path, output_path=None):
        if output_path is None:
            self.writer = None
            self.patterns = Itemsets("FREQUENT ITEMSETS")
        else:
            self.patterns = None
            self.writer = open(output_path, 'w')

        self.startTimestamp = time.time()
        self.itemsetCount = 0
        self.totalCandidateCount = 0
        MemoryLogger().reset()

        self.readInputFile(input_path)

        self.minsupRelative = int(minsup * self.databaseSize)
        self.k = 1

        frequent1 = self.generateFrequent1()

        frequent1.sort()

        if not frequent1 or self.maxPatternLength <= 1:
            self.endTimestamp = time.time()
            MemoryLogger().checkMemory()
            if self.writer:
                self.writer.close()
            return self.patterns

        self.totalCandidateCount += len(frequent1)

        level = None
        self.k = 2
        while True:
            MemoryLogger().checkMemory()
            candidates_k = self.generateCandidateSizeK(frequent1) if self.k > 2 else self.generateCandidate2(frequent1)
            self.totalCandidateCount += len(candidates_k)

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

            level = [candidate for candidate in candidates_k if candidate.get_absolute_support() >= self.minsupRelative]

            if self.k >= self.maxPatternLength + 1 or not level:
                break

            self.k += 1

        self.endTimestamp = time.time()
        MemoryLogger().checkMemory()

        if self.writer:
            self.writer.close()

        return self.patterns

    def readInputFile(self, input_path):
        self.database = []
        map_item_count = {}

        with open(input_path, 'r') as reader:
            for line in reader:
                if line.strip() and not line.startswith(('#', '%', '@')):
                    transaction = [int(item) for item in line.split()]
                    self.database.append(transaction)
                    self.databaseSize += 1

                    for item in transaction:
                        map_item_count[item] = map_item_count.get(item, 0) + 1

        frequent1 = [item for item, count in map_item_count.items() if count >= self.minsupRelative]

        for item in frequent1:
            self.saveItemsetToFile(item, map_item_count[item])

    def generateCandidate2(self, frequent1):
        candidates = []

        for i in range(len(frequent1)):
            item1 = frequent1[i]
            for j in range(i + 1, len(frequent1)):
                item2 = frequent1[j]
                candidates.append(Itemset([item1, item2]))

        return candidates

    def generateCandidateSizeK(self, level_k_1):
        candidates = []

        for i in range(len(level_k_1)):
            itemset1 = level_k_1[i].itemset
            for j in range(i + 1, len(level_k_1)):
                itemset2 = level_k_1[j].itemset

                for k in range(len(itemset1)):
                    if k == len(itemset1) - 1:
                        if itemset1[k] >= itemset2[k]:
                            break
                    elif itemset1[k] < itemset2[k]:
                        continue
                    elif itemset1[k] > itemset2[k]:
                        break

                new_itemset = itemset1 + [itemset2[-1]]

                if self.allSubsetsOfSizeK_1AreFrequent(new_itemset, level_k_1):
                    candidates.append(Itemset(new_itemset))

        return candidates

    def allSubsetsOfSizeK_1AreFrequent(self, candidate, level_k_1):
        for pos_removed in range(len(candidate)):
            found = False
            for subset in level_k_1:
                comparison = ArraysAlgos.sameAs(subset.itemset, candidate, pos_removed)
                if comparison < 0:
                    continue
                elif comparison > 0:
                    found = True
                    break
                else:
                    found = True
                    break

            if not found:
                return False

        return True

    def saveItemset(self, itemset):
        self.itemsetCount += 1

        if self.writer:
            self.writer.write(f"{itemset} #SUP: {itemset.get_absolute_support()}\n")
        else:
            self.patterns.addItemset(itemset, itemset.size())

    def saveItemsetToFile(self, item, support):
        self.itemsetCount += 1

        if self.writer:
            self.writer.write(f"{item} #SUP: {support}\n")
        else:
            itemset = Itemset([item])
            itemset.support = support
            self.patterns.addItemset(itemset, 1)

    def generateFrequent1(self):
        frequent1 = []
        for item, count in map_item_count.items():
            if count >= self.minsupRelative:
                frequent1.append(item)
                self.saveItemsetToFile(item, count)

        return frequent1

    def printStats(self):
        print("============= APRIORI - STATS =============")
        print(f"Candidates count: {self.totalCandidateCount}")
        print(f"The algorithm stopped at size {self.k - 1}")
        print(f"Frequent itemsets count: {self.itemsetCount}")
        print(f"Maximum memory usage: {MemoryLogger().getMaxMemory()} MB")
        print(f"Total time ~ {self.endTimestamp - self.startTimestamp} ms")
        print("===========================================")

    def setMaximumPatternLength(self, length):
        self.maxPatternLength = length

# Example usage:
# algo = AlgoApriori()
# result = algo.runAlgorithm(0.1, 'input_file.txt', 'output_file.txt')
# algo.printStats()
