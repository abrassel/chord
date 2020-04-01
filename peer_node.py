#!/usr/bin/python3
from abstract_node import Node
import constants
from networking import OpCode, sendme

class PeerNode(Node):

    def __init__(self, network, key, owner):
        self.network = network
        self.key = key
        self.owner = owner


    @sendme
    def __setitem__(self, key, value):
        return (OpCode.SET, key, value)


    @sendme
    def __getitem__(self, key):
        return (OpCode.GET, key)


    @sendme
    def find_successor(self, key):
        """
        Obtain the successor node for the given key
        """
        return (OpCode.FIND_SUCCESSOR, key)


    @sendme
    def find_predecessor(self, key):
        """
        Obtain the predecessor node for the given key
        """
        return (Opcode.FIND_PREDECESSOR, key)


    @sendme
    def predecessor(self):
        """
        Return own predecessor node
        """
        return (OpCode.PREDECESSOR,)


    @sendme
    def check(self):
        """
        Determine if this node is alive or not
        """
        return (OpCode.CHECK,)


    @sendme
    def notify_of_leave(self, new_successor):
        """
        Become aware that your successor is leaving.
        Gain a new successor and tell them that you
        are now the predecessor.
        """
        return (OpCode.NOTIFY_OF_LEAVE, self.owner, new_successor)


    @sendme
    def notify(self):
        """
        Be notified by your owner that you
        may have a new predecessor.
        """
        return (OpCode.NOTIFY, self.owner)


    @sendme
    def get_finger_table(self):
        """
        Give the finger table to the caller
        so that they can set up their own.
        """
        return (OpCode.GET_FINGER_TABLE,)


    @sendme
    def give_finger(self, finger):
        """
        Tell this node that their finger
        should be the owner.
        """
        return (GIVE_FINGER, self.owner)


    

    


    
