import socket

'''
Client Server Architecture:
- Messages are sent and received through the server via requests. 

- Each device has an IP address

- When hosting a server, always use local/private IP address. 

- When a device wants to connect to a server in the same LAN, 
it can connect using the private IP address of the server.

- When a device on the internet (not in the same LAN as server) wants
to connectto a server, it must use the public IP address of the server. 

Sockets:
- Socket is basically a communication endpoint. There are many types of 
sockets (internet, bluetooth, infrared, ...)

- The two data transmission protocols are SOCK_STREAM (TCP) and SOCK_DGRAM (UDP).
TCP is used when we want a connection based socket, meaning we establish a connection 
when exchanging messages and terminate it when it's no longer needed
With UDP there is no connection, we just send the message from A to B and that's it. 
'''

HOST = socket.gethostbyname(socket.gethostname()) # private ip address (ethernet adapter)
PORT = 9999

# server is going to be running all the time 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # internet tcp socket 
server.bind((HOST, PORT))

server.listen(5) # only allow accepted 5 connections

while True:
    # accept connections
    # client socket, address of the client socket 
    client, address = server.accept()
    print(f'Connected to {address}')

    # receive the message from the client if we expect one
    message = client.recv(1024).decode('utf-8')
    print(f'Message from client: {message}')

    # send message back to the client 
    client.send('Message received'.encode('utf-8'))

    client.close()
    print(f'Connection with {address} ended')