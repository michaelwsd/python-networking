import socket 
import threading 

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
lock = threading.Lock()

clients = []
nicknames = []

def kick_user(name):
    with lock:
        if name in nicknames:  
            index = nicknames.index(name)
            nicknames.remove(name)
            client = clients.pop(index)
            client.send('You have been kicked by an admin!'.encode('ascii'))
            client.close()
            
            print(f'{name} has disconnected from the chat!')
            broadcast(f'{name} left the chat'.encode('ascii'))

def exit_chat(client):
    # multiple users may exit at the same time
    with lock:
        if client in clients:  
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames.pop(index)
            client.close()
            
            print(f'{nickname} has disconnected from the chat!')
            broadcast(f'{nickname} left the chat'.encode('ascii'))

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            # receive a message and broadcast to all clients
            msg = message = client.recv(1024).decode('ascii')

            if msg.startswith('EXIT'):
                exit_chat(client)
            elif msg.startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin':
                    kick_user(msg[5:])
                else:
                    client.send('Command was refused!'.encode('ascii'))
            elif msg.startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    banned_user = msg[4:]
                    kick_user(banned_user)

                    with open('banned.txt', 'a') as f:
                        f.write(f'{banned_user}\n') 
                else:
                    client.send('Command was refused!'.encode('ascii'))
            else:
                broadcast(message.encode('ascii'))

        # won't hit exception if the client isn't sending
        # exception only raised if connection is closed or network error
        # this is because if the client doesn’t send any data, the recv call just waits forever.
        except:
            exit_chat(client)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {address}')

        # get nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        with open('banned.txt', 'r') as f:
            banned = f.readlines()
        
        # disconnect if banned
        if nickname + '\n' in banned: 
            client.send('BAN'.encode('ascii')) 
            client.close() 
            continue

        # verify admin 
        if nickname == 'admin': 
            client.send('PASS'.encode('ascii')) 
            password = client.recv(1024).decode('ascii') 
            
            # close the connection to this client if pass is incorrect 
            if password != 'password': 
                client.send('REFUSE'.encode('ascii')) 
                client.close() 
                continue

        # add client
        nicknames.append(nickname)
        clients.append(client)
        
        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Successfully connected to the chat!'.encode('ascii'))

        # connect multiple clients at the same time
        # start a single thread of execution for this client
        # args is the arguments passed to the target function, takes an interable
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is listening...')
receive()