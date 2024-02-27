from collections import defaultdict
from itertools import combinations

def load_transactions(input_path):
    transactions = []
    with open(input_path, 'r') as file:
        for line in file:
            transaction = list(map(int, line.strip().split()))
            transactions.append(transaction)
    return transactions

def generate_candidates(itemsets, k):
    candidates = set()
    for itemset1 in itemsets:
        for itemset2 in itemsets:
            if itemset1[:-1] == itemset2[:-1] and itemset1[-1] < itemset2[-1]:
                candidate = itemset1 + (itemset2[-1],)
                candidates.add(candidate)
    return candidates

def has_infrequent_subset(candidate, itemsets, k):
    subsets = list(combinations(candidate, k))
    for subset in subsets:
        if subset not in itemsets:
            return True
    return False

def get_frequent_itemsets(transactions, candidate_itemsets, minsup):
    frequent_itemsets = {}
    counts = defaultdict(int)

    for transaction in transactions:
        for candidate in candidate_itemsets:
            if set(candidate).issubset(transaction):
                counts[candidate] += 1

    num_transactions = len(transactions)
    for candidate, count in counts.items():
        support = count / num_transactions
        if support >= minsup:
            frequent_itemsets[candidate] = count

    return frequent_itemsets

def print_stats(num_transactions, num_frequent_itemsets):
    print("Number of transactions:", num_transactions)
    print("Number of frequent itemsets:", num_frequent_itemsets)

def print_itemsets(itemsets, num_transactions):
    print(" ------- Frequent Itemsets -------")
    for itemset, support in itemsets.items():
        print(f"Pattern: {itemset}  Support: {support} ({support / num_transactions:.2%})")
    print(" ---------------------------------")

def main():
    input_path = "C:\\Users\\INSIGHT\\OneDrive\\Documents\\KCGI\\MP2\\Apriori_java\\src\\contextPasquier99.txt"
    minsup = 0.4

    transactions = load_transactions(input_path)
    
    # Generate frequent 1-itemsets
    frequent_1_itemsets = {}
    for transaction in transactions:
        for item in transaction:
            frequent_1_itemsets[item] += 1

    # Filter 1-itemsets based on minsup
    frequent_1_itemsets = {item: support for item, support in frequent_1_itemsets.items() if support / len(transactions) >= minsup}

    itemsets = frequent_1_itemsets
    k = 2

    while True:
        candidate_itemsets = generate_candidates(itemsets, k)
        frequent_itemsets = get_frequent_itemsets(transactions, candidate_itemsets, minsup)

        if not frequent_itemsets:
            break

        itemsets.update(frequent_itemsets)
        k += 1

    print_stats(len(transactions), len(itemsets))
    print_itemsets(itemsets, len(transactions))

if __name__ == "__main__":
    main()
