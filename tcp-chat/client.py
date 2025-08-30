import socket 
import threading 

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999
nickname = input("Choose a nickname: ")

if nickname == 'admin':
    password = input("Enter password for admin: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

stop_thread = False

def receive():
    global stop_thread

    while not stop_thread:    
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                # set nickname
                client.send(nickname.encode('ascii'))
                # ask for admin password 
                next_message = client.recv(1024).decode('ascii') 
                if next_message == 'PASS': 
                    client.send(password.encode('ascii')) 
                    
                    # check if password is correct 
                    if client.recv(1024).decode('ascii') == 'REFUSE': 
                        print('Connection was refused! Wrong Password') 
                        stop_thread = True

                elif next_message == 'BAN':
                    print('You have been banned from this server!')
                    stop_thread = True 

            else:
                print(message)

        except:
            print('An error occurred!')
            stop_thread = True 
            break

def write():
    global stop_thread

    while not stop_thread:
        try:
            message = f'{nickname}: {input("")}'
            command = message[len(nickname)+2:] 

            if command.startswith('/'):
                if command.startswith('/exit'):
                    client.send('EXIT'.encode('ascii'))
                    print('You have left the chat!')
                    stop_thread = True
                
                elif command.startswith('/kick'):
                    client.send(f'KICK {command[6:]}'.encode('ascii'))
                
                elif command.startswith('/ban'):
                    if nickname == 'admin':
                        client.send(f'BAN {command[5:]}'.encode('ascii'))
                    else:
                        print('This command can only be used by the admin.')
                else:
                    print('Command does not exist.') 
            else:
                client.send(message.encode('ascii'))
        except:
            print('Cannot send, connection closed.')
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()