import socket
import pickle # used to serialize objects to send it over network (decompose to bytes, compose again etc)



class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.178.26"
        self.port = 5555 # has to be the same as in the serverfile
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p


    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
