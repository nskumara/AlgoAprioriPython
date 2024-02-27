from typing import List
import numpy as np

class Itemset:
    def __init__(self, items=None, support=0):
        self.itemset = np.array(items, dtype=int) if items is not None else np.array([], dtype=int)
        self.support = support

    def get_items(self):
        return self.itemset

    def size(self):
        return len(self.itemset)

    def get(self, position):
        return int(self.itemset[position])

    def set_absolute_support(self, support):
        self.support = support

    def get_absolute_support(self):
        return self.support

    def increase_transaction_count(self):
        self.support += 1

    def clone_item_set_minus_one_item(self, item_to_remove):
        new_itemset = np.delete(self.itemset, np.where(self.itemset == item_to_remove))
        return Itemset(new_itemset)

    def clone_item_set_minus_an_itemset(self, itemset_to_not_keep):
        new_itemset = np.setdiff1d(self.itemset, itemset_to_not_keep.itemset)
        return Itemset(new_itemset)

    def intersection(self, itemset2):
        intersection = np.intersect1d(self.itemset, itemset2.itemset)
        return Itemset(intersection)

    def __str__(self):
        return "{" + ", ".join(map(str, self.itemset)) + "}"

    def __eq__(self, other):
        return np.array_equal(self.itemset, other.itemset)

    def __hash__(self):
        return hash(tuple(self.itemset))

# Example Usage:
# itemset1 = Itemset([1, 2, 3], 5)
# itemset2 = Itemset([2, 3, 4], 7)
# intersection_result = itemset1.intersection(itemset2)
# print(intersection_result)
