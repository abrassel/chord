#!/usr/bin/python3


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
                asker.send(func(receiver, asker, *args))

        return send_return
        
