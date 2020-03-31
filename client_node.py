#!/usr/bin/python3

import constants
import Network
from network import remote, Network
from abstract_node import *
from key import Key
from random import randrange
from thread_util import async

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

        self.__notify_ring()  # asynchronous!
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
        if temp_predecessor in interval(self, self.successor, strict_l = True, strict_u = True):
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
        self.__fix_finger(finger)


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
        Find the node queried.
        We go to the closest predecessor of the keyval.
        Afterwards, we are then looking for the successor.
        """
        return self.find_predecessor(self, keyval).successor


    @remote
    def find_predecessor(self, asker, keyval):
        """
        Find the predecessor node.
        We do this by iteratively picking a closer node
        to the correct interval
        """

        if keyval in interval(self, self.successor, True):
            return self

        """
        Successor does not own the key.
        Therefore, let's pick our best guess,
        then ask them to find it.
        """

        for finger in reversed(self.finger_table):
            if finger in interval(self, keyval, True, True):
                return finger.find_predecessor(keyval)

        return self  # this seems like a problem
        

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
        peer_self = Peer(self.networking, self.key, self) # might not have to make a new Peer
        self.predecessor = peer_self
        self.finger_table = [peer_self] * constants.m


    def __init_finger_table(self):
        """
        We borrow a finger table from our successor,
        and use it as hints, going through and modifying entries.
        """
        temp_table = self.successor.get_finger_table()

        for i in range(1, m-1):            
            if start(i) in interval(self, temp_table[i-1], strict_u = True):
                self.finger_table[i] = temp_table[i-1]
            else:
                self.__fix_finger(i)


    @async
    def __fix_finger(self, finger):
        self.finger_table[i] = self.successor.find_successor(start(i))


    def __notify_ring(self):
        """
        Find potential nodes for whom we might be
        in their finger table and alert them.
        """
        for finger in range(m):
            self.find_predecessor(n - start(finger)).give_finger(finger)


    def __take_keys(self):
        """
        Take any keys from the successor that we now own.
        """
        pass  # implement the actual key sharing later
