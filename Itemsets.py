class Itemset:
    def __init__(self, items, support=0):
        self.items = items
        self.support = support

    def get_items(self):
        return self.items

    def get_absolute_support(self):
        return self.support

    def size(self):
        return len(self.items)

    def print_itemset(self):
        print("Items:", self.items)

    def clone_itemset_minus_one_item(self, item_to_remove):
        new_itemset = [item for item in self.items if item != item_to_remove]
        return Itemset(new_itemset)

    def clone_itemset_minus_an_itemset(self, itemset_to_not_keep):
        new_itemset = [item for item in self.items if item not in itemset_to_not_keep]
        return Itemset(new_itemset)

    def intersection(self, itemset2):
        common_items = set(self.items) & set(itemset2.get_items())
        return Itemset(list(common_items), 0)

    def __hash__(self):
        return hash(tuple(self.items))


class ArraysAlgos:
    @staticmethod
    def intersect_two_sorted_arrays(array1, array2):
        set1, set2 = set(array1), set(array2)
        intersection = list(set1 & set2)
        intersection.sort()
        return intersection


class Itemsets:
    def __init__(self, name):
        self.levels = [[]]  # We create an empty level 0 by default.
        self.itemsets_count = 0
        self.name = name

    def print_itemsets(self, nb_object):
        print(" -------", self.name, "-------")
        pattern_count = 0
        level_count = 0
        for level in self.levels:
            print("  L", level_count, "")
            for itemset in level:
                print("  pattern", pattern_count, ":", end=" ")
                itemset.print_itemset()
                print("support:", itemset.get_absolute_support())
                pattern_count += 1
            level_count += 1
        print(" --------------------------------")

    def add_itemset(self, itemset, k):
        while len(self.levels) <= k:
            self.levels.append([])
        self.levels[k].append(itemset)
        self.itemsets_count += 1

    def get_levels(self):
        return self.levels

    def get_itemsets_count(self):
        return self.itemsets_count

    def set_name(self, new_name):
        self.name = new_name

    def decrease_itemset_count(self):
        self.itemsets_count -= 1
