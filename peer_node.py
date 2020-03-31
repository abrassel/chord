#!/usr/bin/python3
from abstract_node import Node
import constants

class PeerNode(Node):

    def __init__(self, network, key, owner):
        self.networking = network
        self.key = key
        self.owner = owner


    def __setitem__(self, key, value):
        pass


    def __getitem__(self, key):
        pass


    def find_successor(self, key):
        """
        Obtain the successor node for the given key
        """
        pass


    def predecessor(self):
        """
        Return own predecessor node
        """
        pass


    def check(self):
        """
        Determine if this node is alive or not
        """
        pass


    def notify_of_leave(self, new_successor):
        """
        Become aware that your successor is leaving.
        Gain a new successor and tell them that you
        are now the predecessor.
        """
        pass


    def notify(self):
        """
        Be notified by your owner that you
        may have a new predecessor.
        """
        pass


    

    


    
