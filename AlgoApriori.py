import time

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

    def addItemset(self, itemset, size):
        if size not in self.itemsets:
            self.itemsets[size] = []
        self.itemsets[size].append(itemset)

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

    def runAlgorithm(self, minsup, input_file, output_file=None):
        if output_file is None:
            self.writer = None
            self.patterns = Itemsets("FREQUENT ITEMSETS")
        else:
            self.patterns = None
            self.writer = open(output_file, "w")

        self.startTimestamp = int(round(time.time() * 1000))
        self.itemsetCount = 0
        self.totalCandidateCount = 0
        MemoryLogger.getInstance().reset()

        database = []
        map_item_count = {}

        with open(input_file, "r") as reader:
            for line in reader:
                if line.strip() == "" or line[0] in ['#', '%', '@']:
                    continue

                line_splited = line.split()
                transaction = [int(item) for item in line_splited]

                for item in transaction:
                    if item in map_item_count:
                        map_item_count[item] += 1
                    else:
                        map_item_count[item] = 1

                database.append(transaction)
                self.databaseSize += 1

        self.minsupRelative = int(minsup * self.databaseSize)
        self.k = 1

        frequent1 = [item for item, count in map_item_count.items() if count >= self.minsupRelative]
        frequent1.sort()

        if not frequent1 or self.maxPatternLength <= 1:
            self.endTimestamp = int(round(time.time() * 1000))
            MemoryLogger.getInstance().checkMemory()

            if self.writer is not None:
                self.writer.close()

            return self.patterns

        self.totalCandidateCount += len(frequent1)

        level = None
        self.k = 2
        while True:
            MemoryLogger.getInstance().checkMemory()

            if self.k == 2:
                candidates_k = self.generate_candidate_2(frequent1)
            else:
                candidates_k = self.generate_candidate_size_k(level)

            self.totalCandidateCount += len(candidates_k)

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
            if self.k < self.maxPatternLength + 1:
                for candidate in candidates_k:
                    if candidate.support >= self.minsupRelative:
                        level.append(candidate)
                        self.save_itemset(candidate)

            if not level:
                break

            self.k += 1

        self.endTimestamp = int(round(time.time() * 1000))
        MemoryLogger.getInstance().checkMemory()

        if self.writer is not None:
            self.writer.close()

        return self.patterns

    def getDatabaseSize(self):
        return self.databaseSize

    def generate_candidate_2(self, frequent1):
        candidates = []

        for i in range(len(frequent1)):
            item1 = frequent1[i]
            for j in range(i + 1, len(frequent1)):
                item2 = frequent1[j]
                candidates.append(Itemset([item1, item2]))

        return candidates

    def generate_candidate_size_k(self, level_k_1):
        candidates = []

        for i in range(len(level_k_1)):
            itemset1 = level_k_1[i].itemset
            for j in range(i + 1, len(level_k_1)):
                itemset2 = level_k_1[j].itemset

                for k in range(len(itemset1)):
                    if k == len(itemset1) - 1:
                        if itemset1[k] >= itemset2[k]:
                            continue
                    elif itemset1[k] < itemset2[k]:
                        continue
                    elif itemset1[k] > itemset2[k]:
                        break

                new_itemset = itemset1 + [itemset2[-1]]

                if self.all_subsets_of_size_k_1_are_frequent(new_itemset, level_k_1):
                    candidates.append(Itemset(new_itemset))

        return candidates

    def all_subsets_of_size_k_1_are_frequent(self, candidate, level_k_1):
        for pos_removed in range(len(candidate)):
            found = False

            first = 0
            last = len(level_k_1) - 1

            while first <= last:
                middle = (first + last) >> 1

                comparison = ArraysAlgos.sameAs(level_k_1[middle].itemset, candidate, pos_removed)

                if comparison < 0:
                    first = middle + 1
                elif comparison > 0:
                    last = middle - 1
                else:
                    found = True
                    break

            if not found:
                return False

        return True

    def save_itemset(self, itemset):
        self.itemsetCount += 1

        if self.writer is not None:
            self.writer.write(str(itemset) + " #SUP: " + str(itemset.support) + "\n")
        else:
            self.patterns.addItemset(itemset, len(itemset.itemset))

    def save_itemset_to_file(self, item, support):
        self.itemsetCount += 1

        if self.writer is not None:
            self.writer.write(str(item) + " #SUP: " + str(support) + "\n")
        else:
            itemset = Itemset([item])
            itemset.support = support
            self.patterns.addItemset(itemset, 1)

    def print_stats(self):
        print("=============  APRIORI - STATS =============")
        print(" Candidates count : " + str(self.totalCandidateCount))
        print(" The algorithm stopped at size " + str(self.k - 1))
        print(" Frequent itemsets count : " + str(self.itemsetCount))
        print(" Maximum memory usage : " + str(MemoryLogger.getInstance().getMaxMemory()) + " mb")
        print(" Total time ~ " + str(self.endTimestamp - self.startTimestamp) + " ms")
        print("===================================================")

    def set_maximum_pattern_length(self, length):
        self.maxPatternLength = length
