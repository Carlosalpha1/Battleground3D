import socket
import sys
import select
import time, threading

MSG_SIZE = 4096
HANDSHAKE_MSG = b'NEW_CONNECTION'


class Client:

    def __init__(self, server_ip, server_port):
        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_address = (server_ip, server_port)
        self.recv_thread = None
        self.reception_module = False

        self.sockfd.setblocking(False)

        self.__initSocket()
    

    def __initSocket(self):
        try:
            self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as msg:
            print("socket.socket() failed:", msg, file=sys.stderr)
            self.__raiseException()
    

    def __raiseException(self):
        raise ClientException()

    
    def __receptionThread(self):
        while self.reception_module:
            print("reception thread")
            time.sleep(1)


    def initHandshake(self):
        timeout = 2
        self.send(HANDSHAKE_MSG)
        
        ready = select.select([self.sockfd], [], [], timeout)
        if ready[0]:
            data, address = self.recv(MSG_SIZE)
            if data == b'NEW_CONNECTION_ACK' and address == self.server_address:
                return True
            elif data == b'CONNECTION DENIED' and address == self.server_address:
                return False
        self.__raiseException()
        
        return None
    
    
    def initReceptionModule(self):
        self.reception_module = True
        self.recv_thread = threading.Thread(name='Receive Module', target=self.__receptionThread)
        self.recv_thread.start()
    

    def stopReceptionModule(self):
        self.reception_module = False
        if self.recv_thread != None:
            self.recv_thread.join()
    

    def send(self, data, address = self.server_address):
        self.sockfd.sendto(data, self.server_address)
    
    
    def recv(self, msg_size):
        return self.sockfd.recvfrom(msg_size)
    

    def closeConnection(self):
        self.send(b'CLOSE_CONNECTION')


    def shutdown(self):
        self.stopReceptionModule()
        self.sockfd.close()


class ClientException(Exception):

    def __init__(self):
        self.message = "Client Failure"
        super().__init__(self.message)



if __name__ == "__main__":

    try:
        client = Client("127.0.0.1", 34343)
        connected = client.initHandshake()
        if connected:
            client.initReceptionModule()
            while True:
                time.sleep(0.5)
                print("processing")
        else:
            print("Connection Denied")
        
    except KeyboardInterrupt:
        client.shutdown()
        sys.exit(0)

    except ClientException:
        client.shutdown()
        sys.exit(1)
    
    finally:
        client.shutdown()
        sys.exit(0)
    
    