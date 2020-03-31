#!/usr/bin/python3
from abc import ABC

def start(i):
    return 2**i


class Interval:

    def __init__(self, lower, upper, strict_l = False, strict_u = False):
        self.interval = (lower, upper)
        self.strict_l = strict_l
        self.strict_u = strict_u

    def __contains__(self, value):
        if (
                strict_l && self.interval[0] == value or
                strict_r && self.interval[1] == value
        ):
            return False

        return self.interval[0] <= value and self.interval[1] >= value

    
class Node(ABC):

    @abstractmethod
    def __getitem__(self, key):
        """
        get an existing value using the passed key
        """
        pass


    @abstractmethod
    def __setitem__(self, key, newval):
        """
        put an item in the keyset (or pass it on)
        """
        pass


    def __lt__(self, other):
        return self.key < other.key


    def __le__(self, other):
        return self.key <= other.key

    
    def __eq__(self, other):
        return self.key == other.key


    def __ne__(self, other):
        return self.key != other.key


    def __ge__(self, other):
        return self.key >= other.key


    def __gt__(self, other):
        return self.key > other.key
