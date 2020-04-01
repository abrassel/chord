#!/usr/bin/python3

from enum import Enum, unique

@unique
class OpCode(Enum):
    SET = "0"
    GET = "1"
    FIND_SUCCESSOR = "2"
    FIND_PREDECESSOR = "3"
    PREDECESSOR = "4"
    CHECK = "5"
    NOTIFY_OF_LEAVE = "6"
    NOTIFY = "7"
    GET_FINGER_TABLE = "8"
    GIVE_FINGER = "9"

response_required = set(
    OpCode.GET,
    OpCode.FIND_SUCCESSOR,
    OpCode.FIND_PREDECESSOR,
    OpCode.PREDECESSOR,
    OpCode.CHECK,
    OpCode.GET_FINGER_TABLE
)


# TODO: multi-thread acceptance and sending.
class Network:

    def __init__(self, ip, host, owner_ip = None, owner_host = None):
        self.ip = ip
        self.host = host


        if not owner_ip or not owner_host:
            self.__setup_networking()
        
        
        if dest_ip and dest_host:
            self.__create_connection()
            
        
    def tcp_send(self, message):
        """
        Send the message to the node.  Guarantee arrival.
        """
        pass


    def udp_send(self, message):
        """
        Send the message to the node.  No guarantees about arrival.
        """
        pass


    def await_response(self):
        """
        Get a response from  the node on the far side.
        """
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
        """
        Sends the parameters given to the remote node
        """
        
        def wrapper(peer, args):
            result = func(peer, args)
            opcode = result[0]
            message = serialize(result)
            peer.network.tcp_send(message)
            if opcode in response_required:
                return deserialize(opcode, peer.network.wait_response())
            else:
                peer.network.udp_send(opcode, message)

        return wrapper
        

    @staticmethod
    def serialize(args):
        result = ""
        for arg in args:
            if isinstance(arg, str):
                result += arg
            elif isinstance(arg, Node):
                result += (
                    arg.networking.ip
                    + "|" + arg.networking.host
                    + "|" + arg.key
                )
            else:
                result += arg.serialize()

            result += "|"

        return result[:-1]  # truncate last separator


    @staticmethod
    def unserialize(opcode, response):
        pass
        

    def __create_connection(self):
        """
        Used when this is a peer
        and want to abstract connection to it.
        """
        pass


    def __setup_networking(self):
        """
        Used when you own the host, port.
        Bind to it so that others can connect to you.
        """
        pass
