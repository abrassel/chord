#!/usr/bin/python3
from hashlib import sha1

class Key:

    def __init__(self, keyval):
        self.key = keyval
        self.hash_val = int(sha1(keyval).hexdigest(), 16)
        

    def __hash__(self):
        """
        Store the hash for efficient lookup.
        """
        return self.hash_val
