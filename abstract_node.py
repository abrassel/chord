#!/usr/bin/python3
from abc import ABC

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
