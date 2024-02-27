import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

public class Itemset extends AbstractOrderedItemset {
    public int[] itemset;
    public int support = 0;

    public Itemset() {
        itemset = new int[]{};
    }

    public Itemset(int item) {
        itemset = new int[]{item};
    }

    public Itemset(int[] items) {
        this.itemset = items;
    }

    public Itemset(List<Integer> itemset, int support) {
        this.itemset = new int[itemset.size()];
        int i = 0;
        for (Integer item : itemset) {
            this.itemset[i++] = item.intValue();
        }
        this.support = support;
    }

    public int[] getItems() {
        return itemset;
    }

    public int getAbsoluteSupport() {
        return support;
    }

    public int size() {
        return itemset.length;
    }

    public Integer get(int position) {
        return itemset[position];
    }

    public void setAbsoluteSupport(Integer support) {
        this.support = support;
    }

    public void increaseTransactionCount() {
        this.support++;
    }

    public Itemset cloneItemSetMinusOneItem(Integer itemToRemove) {
        int[] newItemset = new int[itemset.length - 1];
        int i = 0;
        for (int j = 0; j < itemset.length; j++) {
            if (itemset[j] != itemToRemove) {
                newItemset[i++] = itemset[j];
            }
        }
        return new Itemset(newItemset);
    }

    public Itemset cloneItemSetMinusAnItemset(Itemset itemsetToNotKeep) {
        int[] newItemset = new int[itemset.length - itemsetToNotKeep.size()];
        int i = 0;
        for (int j = 0; j < itemset.length; j++) {
            if (!itemsetToNotKeep.contains(itemset[j])) {
                newItemset[i++] = itemset[j];
            }
        }
        return new Itemset(newItemset);
    }

    public Itemset intersection(Itemset itemset2) {
        int[] intersection = ArraysAlgos.intersectTwoSortedArrays(this.getItems(), itemset2.getItems());
        return new Itemset(intersection);
    }

    @Override
    public int hashCode() {
        return Arrays.hashCode(itemset);
    }
}

class ArraysAlgos {
    public static int[] cloneItemSetMinusOneItem(int[] itemset, Integer itemToRemove) {
        int[] newItemset = new int[itemset.length - 1];
        int i = 0;
        for (int j = 0; j < itemset.length; j++) {
            if (itemset[j] != itemToRemove) {
                newItemset[i++] = itemset[j];
            }
        }
        return newItemset;
    }

    public static int[] cloneItemSetMinusAnItemset(int[] itemset, int[] itemsetToNotKeep) {
        int[] newItemset = new int[itemset.length - itemsetToNotKeep.length];
        int i = 0;
        for (int j = 0; j < itemset.length; j++) {
            if (Arrays.binarySearch(itemsetToNotKeep, itemset[j]) < 0) {
                newItemset[i++] = itemset[j];
            }
        }
        return newItemset;
    }

    public static boolean allTheSameExceptLastItem(int[] itemset1, int[] itemset2) {
        for (int i = 0; i < itemset1.length - 1; i++) {
            if (itemset1[i] != itemset2[i]) {
                return false;
            }
        }
        return true;
    }

    public static int[] concatenate(int[] prefix, int[] suffix) {
        int[] concatenation = new int[prefix.length + suffix.length];
        System.arraycopy(prefix, 0, concatenation, 0, prefix.length);
        System.arraycopy(suffix, 0, concatenation, prefix.length, suffix.length);
        return concatenation;
    }

    public static int[] intersectTwoSortedArrays(int[] array1, int[] array2) {
        int newArraySize = (array1.length < array2.length) ? array1.length : array2.length;
        int[] newArray = new int[newArraySize];
        int pos1 = 0;
        int pos2 = 0;
        int posNewArray = 0;
        while (pos1 < array1.length && pos2 < array2.length) {
            if (array1[pos1] < array2[pos2]) {
                pos1++;
            } else if (array2[pos2] < array1[pos1]) {
                pos2++;
            } else {
                newArray[posNewArray] = array1[pos1];
                posNewArray++;
                pos1++;
                pos2++;
            }
        }
        return Arrays.copyOfRange(newArray, 0, posNewArray);
    }

    public static boolean containsOrEquals(Integer[] itemset1, Integer[] itemset2) {
        loop1:
        for (int i = 0; i < itemset2.length; i++) {
            for (int j = 0; j < itemset1.length; j++) {
                if (itemset1[j].intValue() == itemset2[i].intValue()) {
                    continue loop1;
                } else if (itemset1[j].intValue() > itemset2[i].intValue()) {
                    return false;
                }
            }
            return false;
        }
        return true;
    }

    public static boolean containsOrEquals(Short[] itemset1, Short[] itemset2) {
        loop1:
        for (int i = 0; i < itemset2.length; i++) {
            for (int j = 0; j < itemset1.length; j++) {
                if (itemset1[j].shortValue() == itemset2[i].shortValue()) {
                    continue loop1;
                } else if (itemset1[j].shortValue() > itemset2[i].shortValue()) {
                    return false;
                }
            }
            return false;
        }
        return true;
    }

    public static boolean containsOrEquals(List<Short> itemset1, List<Short> itemset2) {
        loop1:
        for (int i = 0; i < itemset2.size(); i++) {
            short val2 = itemset2.get(i);
            for (int j = 0; j < itemset1.size(); j++) {
                short val1 = itemset1.get(j);
                if (val1 == val2) {
                    continue loop1;
                } else if (val1 > val2) {
                    return false;
                }
            }
            return false;
        }
        return true;
    }

    public static boolean containsLEX(Integer[] itemset, Integer item, int maxItemInArray) {
        if (item > maxItemInArray) {
            return false;
        }
        for (Integer itemI : itemset) {
            if (itemI.equals(item)) {
                return true;
            } else if (itemI > item) {
                return false;
            }
        }
        return false;
    }

    public static int[] sameAs(int[] itemset1, int[] itemsets2, int posRemoved) {
        int j = 0;
        for (int i = 0; i < itemset1.length; i++) {
            if (j == posRemoved) {
                j++;
            }
            if (itemset1[i] == itemsets2[j]) {
                j++;
            } else if (itemset1[i] > itemsets2[j]) {
                return 1;
            } else {
                return -1;
            }
        }
        return 0;
    }

    public static boolean includedIn(int[] itemset1, int[] itemset2) {
        int count = 0;
        for (int i = 0; i < itemset2.length; i++) {
            if (itemset2[i] == itemset1[count]) {
                count++;
                if (count == itemset1.length) {
                    return true;
                }
            }
        }
        return false;
    }

    public static boolean includedIn(int[] itemset1, int itemset1Length, int[] itemset2) {
        int count = 0;
        for (int i = 0; i < itemset2.length; i++) {
            if (itemset2[i] == itemset1[count]) {
                count++;
                if (count == itemset1Length) {
                    return true;
                }
            }
        }
        return false;
    }

    public static boolean containsLEXPlus(int[] itemset, int item) {
        for (int i = 0; i < itemset.length; i++) {
            if (itemset[i] == item) {
                return true;
            } else if (itemset[i] > item) {
                return true;
            }
        }
        return false;
    }

    public static boolean containsLEX(int[] itemset, int item) {
        for (int i = 0; i < itemset.length; i++) {
            if (itemset[i] == item) {
                return true;
            } else if (itemset[i] > item) {
                return false;
            }
        }
        return false;
    }

    public static boolean contains(int[] itemset, int item) {
        for (int i = 0; i < itemset.length; i++) {
            if (itemset[i] == item) {
                return true;
            } else if (itemset[i] > item) {
                return false;
            }
        }
        return false;
    }

    public static Comparator<int[]> comparatorItemsetSameSize = new Comparator<int[]>() {
        @Override
        public int compare(int[] itemset1, int[] itemset2) {
            for (int i = 0; i < itemset1.length; i++) {
                if (itemset1[i] < itemset2[i]) {
                    return -1;
                } else if (itemset2[i] < itemset1[i]) {
                    return 1;
                }
            }
            return 0;
        }
    };

    public static int[] appendIntegerToArray(int[] array, int integer) {
        int[] newgen = new int[array.length + 1];
        System.arraycopy(array, 0, newgen, 0, array.length);
        newgen[array.length] = integer;
        return newgen;
    }

    public static double[] convertStringArrayToDoubleArray(String[] tokens) {
        double[] numbers = new double[tokens.length];
        for (int i = 0; i < tokens.length; i++) {
            numbers[i] = Double.parseDouble(tokens[i]);
        }
        return numbers;
    }

    public static boolean isSubsetOf(List<Short> itemset1, Short[] itemset2) {
        if (itemset1 == null || itemset1.size() == 0) {
            return true;
        }
        for (short val : itemset1) {
            boolean found = false;
            for (short value : itemset2) {
                if (value > val) {
                    return false;
                } else if (val == value) {
                    found = true;
                    break;
                }
            }
            if (!found)
                return false;
        }
        return true;
    }

    public static Short[] concatenate(Short[] itemset1, Short[] itemset2) {
        Short[] concatenation = new Short[itemset1.length + itemset2.length];
        System.arraycopy(itemset1, 0, concatenation, 0, itemset1.length);
        System.arraycopy(itemset2, 0, concatenation, itemset1.length, itemset2.length);
        return concatenation;
    }
}
