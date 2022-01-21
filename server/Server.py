import socket
import sys
import threading
import settings

MSG_SIZE = 4096

class Server:

    def __init__(self, host, port):
        
        self.sockfd = None
        self.host = host
        self.port = port
        
        self.clients = []
        self.max_clients = settings.MAX_CLIENTS
        self.num_clients = 0

        self.__initSocket()
        self.__makeBind()
    

    def __initSocket(self):
        try:
            self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as msg:
            print("socket.socket() failed:", msg, file=sys.stderr)
            self.__raiseException()
    

    def __makeBind(self):
        try:
            self.sockfd.bind((self.host, self.port))
        except socket.error as msg:
            print("socket.bind() failed:", msg, file=sys.stderr)
            self.__raiseException()
    

    def __raiseException(self):
        raise ServerException()


    def __isRegistered(self, address):
        return address in self.clients
    

    def appendClient(self, address):
        if self.num_clients < self.max_clients:
            self.clients.append(address)
            self.num_clients += 1
            return True
        return False
    

    def removeClient(self, address):
        if address in self.clients:
            self.clients.remove(address)
            self.num_clients -= 1
            return True
        return False
    

    def send(self, data, address):
        self.sockfd.sendto(data, address)


    def recv(self, msg_size):
        return self.sockfd.recvfrom(msg_size)
    

    def setNewConnection(self, address):
        if not self.__isRegistered(address) and self.num_clients < self.max_clients:
            print("a")
            self.appendClient(address)
            self.send(b'NEW_CONNECTION_ACK', address)
        else:
            print("b")
            self.send(b'CONNECTION DENIED', address)
    

    def closeConnection(self, address):
        self.removeClient(address)
    

    def shutdown(self):
        self.sockfd.close()
            


class ServerException(Exception):

    def __init__(self):
        self.message = "Server Failure"
        super().__init__(self.message)


if __name__ == "__main__":

    try:
        server = Server(settings.HOST, settings.PORT)
        while True:
            data, address = server.recv(MSG_SIZE)
            data = data.split()
            if data[0] == b'NEW_CONNECTION':
                server.setNewConnection(address)
            elif data[0] == b'CLIENT_DATA':
                print("do something")
            elif data[0] == b'CLOSE_CONNECTION':
                server.removeClient(address)
            
            print(server.clients)
            

    except KeyboardInterrupt:
        server.shutdown()
        print("\nExit Success")
        sys.exit(0)

    except ServerException as msg:
        server.shutdown()
        print(msg, file=sys.stderr)
        sys.exit(1)
