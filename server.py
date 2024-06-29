import pickle
import threading
import socket
from Files.PDF_file import PDF_file
from Files.PNG_file import PNG_file

HOST = '127.0.0.1'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []
files = []

# DO NOT TOUCH
def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def Send_file(client):
    files_message = "\n".join(file.display() for file in files)
    client.send(files_message.encode('utf-8'))

def Send_user(client):
    users_message = "\n".join(f"User: {user}" for user in nicknames)
    client.send(users_message.encode('utf-8'))

def Broadcast(message):
    for client in clients:
        client.send(message)

def De_serialize(serialized_file):
    return pickle.loads(serialized_file)

# PRAY TO GOD THIS WORKS
# IF IT DOESNT YOU ARE IN HELL
def Handle(client):
    while True:
        try:
            message = client.recv(1024)
            if message.startswith(b'OBJ:'):
                # This is a serialized object
                serialized_obj = message[4:]
                obj = pickle.loads(serialized_obj)
                files.append(obj)
            else:
                # This is a simple message
                message = message.decode('utf-8')
                command = message.split(": ")[1].upper()
                if command == "!FILES":
                    Send_file(client)
                elif command == "!USERS":
                    Send_user(client)
                else:
                    Broadcast(message.encode('utf-8'))
        except Exception as e:
            print(f"Exception in Handle: {e}")
            if client in clients:
                clientIndex = clients.index(client)
                clients.remove(client)
                nickname = nicknames[clientIndex]
                Broadcast(f"{nickname} got killed".encode('utf-8'))
                nicknames.remove(nickname)

            break

def Receive():
    while True:
        client, address = server.accept()
        print(f"{str(address)} has connected")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode("utf-8")

        nicknames.append(nickname)
        clients.append(client)

        print(f"Client nickname is {nickname}")
        Broadcast(f"{nickname} has joined the chat!".encode('utf-8'))
        client.send("You are connected!".encode('utf-8'))

        thread = threading.Thread(target=Handle, args=(client,))
        thread.start()

print("Server is up!")
Receive()