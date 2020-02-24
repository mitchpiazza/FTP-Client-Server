import socket
import os

LOCALHOST = "127.0.0.1"
PORT = 8085
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((LOCALHOST, PORT))
server.listen(10)
print("Server started")
print("Waiting for client request...")
msg = ''
path = os.getcwd()
clientConnection, clientAddress = server.accept()
print("Connected client :" , clientAddress)
while True:
    in_data = clientConnection.recv(1024)
    msg = in_data.decode()
    if msg == 'quit':
        print("client connection terminated")
        clientConnection, clientAddress = server.accept()
        print("Connected client :" , clientAddress)
    elif msg.split(' ')[0] == "List":
        files = os.listdir(path)
        file_string = ''
        for f in files:
            file_string += f
            file_string += ', '
        clientConnection.send(bytes(file_string,'UTF-8'))
        print("List Sent to User")
    elif msg.split(' ')[0] == "retrieve":
        fileName = msg.split(' ')[1]
        if os.path.isfile(fileName):
            with open(fileName, 'rb') as f:
                contents = f.read(1024)
                while contents:
                    clientConnection.send(contents)
                    contents = f.read(1024)
                print("File Sent to User")
                clientConnection.send(bytes("end", "UTF-8"))
            f.close()
        else:
            clientConnection.send(bytes("No file found","UTF-8"))
    elif msg.split(' ')[0] == "store":
        f = open(msg.split(' ')[1], 'wb')
        buff = clientConnection.recv(1024)
        while buff:
            nextItem = clientConnection.recv(1024)
            if nextItem.decode().endswith("end"):
                buff += nextItem[0:len(nextItem) - 3]
                break
            else:
                buff += nextItem  
        print("File Stored on Server")
        f.write(buff)
        f.close()
        msg = buff.decode()
    else:
        print("Not a valid command, please input another command")
        clientConnection.send(bytes("Not a Valid command","UTF-8"))

print("Client disconnected...")
clientConnection.close()