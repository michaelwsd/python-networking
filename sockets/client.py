import socket 

# if we are not in the same LAN, we need the public IP address of the server
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT)) # connect to server

socket.send('Hello World'.encode('utf-8')) # send message to server 
print(socket.recv(1024).decode('utf-8')) # receive a message back from the server