#!/usr/bin/python3

import constants
import Network
from Network import remote, Network
from abstract_node import *
from key import Key
from random import randrange

class ClientNode(Node):


    def __init__(self):
        self.items = {}
        self.finger_table = [None] * constants.m
        self.predecessor = None
        self.network = Network()
        self.key = Key(self.network.ip)
    

    ###########################################
    ############ ACTIVE METHODS ###############
    ###########################################

    def __setitem__(self, key, newvalue):
        key = Key(self.key)
        if key in self.items:
            self.items[key] = newvalue
        else:
            self.find_successor(key)[key] = newvalue  # inefficient but pretty


    def __setattr__(self, name, value):
        if name == "successor":
            self.finger_table[0] = value


    def __getattr__(self, name):
        if name == "successor":
            # this may fail if successor has dropped from network
            return self.finger_table[0]


    def join(self, sister):
        """
        When a new Node joins a network it has to do several things:
        1. Find its predecessor.
        2. Construct its finger table.
        3. Notify other nodes that it exists (update pred and fin_tables).
        4. Take control of its new keys.
        5. If there is no sister, we are starting a new ring
        """
        if not sister:
            self.__start_ring()
            return

        self.successor = sister.find_successor(start(0))
        self.predecessor = self.successor.predecessor
        self.__init_finger_table()  # already constructed first entry

        self.__notify_ring()  # asynchronious!
        self.__take_keys()


    def leave(self):
        """
        When a Node leaves a network, it is responsible for the following actions:
        1. Send a predecessor its successor
        2. Send a successor its new predecessor
        3. Give up its keys to its successor
        """
        if not self.predecessor:
            return  # what do here?
        
        self.predecessor.notify_of_leave(self.successor)  # notifies successor
        self.successor.give_keys(self.keys)
        

    def __trigger_stabilization(self):
        """
        Each node should periodically run this stabilization routine.
        """
        
        self.__stabilize()
        self.__notify()
        self.__fix_fingers()

        if not self.predecessor.check():
            self.predecessor = None
    

    def __stabilize(self):
        """
        Determine if you have the correct successor
        """
        
        temp_predecessor = self.successor.predecessor
        if temp_predecessor in interval(self, self.successor):
            self.successor = temp_predecessor
            temp_predecessor.notify()


    def __notify(self):
        """
        Tell your successor that you exist
        """
        
        self.successor.notify()


    def __fix_fingers(self):
        """
        Update a random entry in the finger table
        """
        
        finger = randrange(constants.m)
        self.finger_table[finger] = self.find_successor(self, start(finger))


    ###########################################
    ########### PASSIVE METHODS ###############
    ###########################################
    """
    Remote calls that this node receives
    """
    
    @remote
    def __getitem__(self, asker, keyval):
        """
        Finds the key queried
        """
        key = Key(keyval)        
        return self.find_successor(self, key)[key]


    @remote
    def find_successor(self, asker, keyval):
        """
        Find the node queried
        """
        pass


    ###########################################
    ############# BACKING METHODS #############
    ###########################################
    """
    Any calls / functions that this node generates
    or receives that are not
    explicitly top level calls in the chord paper.
    """

    def __start_ring(self):
        """
        In this case, you are the first.  Congratulations!
        This means that you get to be all of your own fingers,
        etc.
        """
        peer_self = Peer(self.networking, self.key, self)
        self.predecessor = peer_self
        self.finger_table = [peer_self] * constants.m


    def __init_finger_table(self):
        """
        We borrow a finger table from our successor,
        and use it as hints, going through and modifying entries.
        """
        pass


    def __notify_ring(self):
        """
        Find potential nodes for whom we might be
        in their finger table and alert them.
        """
        pass


    def __take_keys(self):
        """
        Take any keys from the successor that we now own.
        """
        pass
