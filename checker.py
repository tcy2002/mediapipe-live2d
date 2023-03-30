import socket
import sys


class Checker:
    def __init__(self, addr, port):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.listener.bind((addr, port))
        except Exception as e:
            sys.exit(0)

    def __del__(self):
        self.listener.close()
