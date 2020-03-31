#!/usr/bin/python3

from enum import Enum, unique

@unique
class OpCode(Enum):
    SET = 0
    GET = 1
    FIND_SUCCESSOR = 2
    FIND_PREDECESSOR = 3
    PREDECESSOR = 4
    CHECK = 5
    NOTIFY_OF_LEAVE = 6
    NOTIFY = 7
    GET_FINGER_TABLE = 8
    GIVE_FINGER = 9

response_required = set(
    OpCode.GET,
    OpCode.FIND_SUCCESSOR,
    OpCode.FIND_PREDECESSOR,
    OpCode.PREDECESSOR,
    OpCode.CHECK,
    OpCode.GET_FINGER_TABLE
)
    
class Network:

    def __init__(self):
        pass


    @staticmethod
    def remote(func):
        """
        Decorator that changes return to send
        """
        def send_return(receiver, asker, *args):
            if receiver == asker:
                return func(receiver, asker, *args)
            else:
                asker.network.send(func(receiver, asker, *args))

        return send_return


    @staticmethod
    def sendme(func):
        def wrapper(peer, args):
            opcode = func(peer, args)
            if opcode in response_required:
                peer.network.tcp_send(args)
                return peer.network.wait_response()
            else:
                peer.network.udp_send(args)

        return wrapper
        
