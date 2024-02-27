from abc import ABC, abstractmethod
from decimal import Decimal

class AbstractItemset(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    def print_itemset(self):
        print(str(self), end="")

    @abstractmethod
    def get_absolute_support(self):
        pass

    @abstractmethod
    def get_relative_support(self, nb_object):
        pass

    def get_relative_support_as_string(self, nb_object):
        frequence = self.get_relative_support(nb_object)
        return '{:.5f}'.format(frequence)

    @abstractmethod
    def contains(self, item):
        pass
