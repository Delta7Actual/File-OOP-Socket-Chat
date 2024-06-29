import pickle
import threading
import socket
from Files.PDF_file import PDF_file
from Files.PNG_file import PNG_file

HOST = '127.0.0.1'
PORT = 55555

print("WELCOME TO OOPFC! Type !help for commands!")
nickname = input("Enter nickname: ").strip()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def Receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "NICK":
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Failed to connect")
            client.close()
            break

def PDF():
    name = input(">>> Name: ")
    size = input(">>> Size: ")
    body = input(">>> Body: ")

    pdf = PDF_file(name, size, nickname, body)
    serialized_pdf = b'OBJ:' + pickle.dumps(pdf)
    client.sendall(serialized_pdf)

def PNG():
    name = input(">>> Name: ")
    size = input(">>> Size: ")
    resolution = input(">>> Resolution: ")
    png = PNG_file(name,size,resolution)
    serialized_png = b'OBJ:' + pickle.dumps(png)
    client.sendall(serialized_png)

def Send():
    while True:
        message = f'{nickname}: {input()}'
        command = message.split(": ")[1].upper()
        if command == '!HELP':
            print(">>> The commands are: !pdf, !png, !files and !users")
        elif command == '!PDF':
            PDF()
        elif command == '!PNG':
            PNG()
        else:
            client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=Receive)
receive_thread.start()

send_thread = threading.Thread(target=Send)
send_thread.start()