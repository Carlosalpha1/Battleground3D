# Client API

### Constructor: Client(server_ip, port)
* It creates a Client class with the ip and port of the server. It adjusts some parameters

### client.initHandshake()
* It exchanges connection establishment messages. Only it must be called once.
* Returns:  
  * **True** -> Connection Accepted
  * **False** -> Connection Denied
  * **None** -> Unknown. It raises a ClientException()

### client.initReceptionModule()
* It activates the Reception Module Thread working in background. Only it must be called once or after being stopped with _stopReceptionModule()_ method.

### client.stopReceptionModule()
* It stops the Reception Module Thread. Only it must be called once same as _initReceptionModule()_

### client.send(data, address)
* It send a data to address. The default address is the server ip indicated in the Constructor.

### client.recv(msg_size)
* It receives a message from socket of size _msg_size_ maximum.

### client.closeConnection()
* It closes a Connection with the Server sending a message CLOSE_CONNECTION.

### client.shutdown()
* It stops all subprocess of client running and close the socket.
