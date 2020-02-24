import socket
import os
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def connect_to_server(server, port, client):
    client.connect((server, port))
    
path = os.getcwd()
print("Please input \"connect <IP Address> <Port Number>\": ")
connectflag = False
while True:
    cmd_input = input()
    if cmd_input.split(' ')[0] == "connect" and connectflag == False:
        connect_to_server(cmd_input.split(' ')[1], int(cmd_input.split(' ')[2]), client) 
        connectflag = True
        print("Commands: list, retrieve <filename>, store <filename>, quit")
    elif cmd_input == "list":
        client.sendall(bytes("List",'UTF-8'))
        buff = client.recv(1024)
        msg = buff.decode()
        print("List of files in directory:\n" + msg)
    elif cmd_input.split(' ')[0] == "retrieve":
        client.sendall(bytes(cmd_input, 'UTF-8'))
        buff = client.recv(1024)
        if buff.decode() == "No file found":
            print("Invalid file")
        else:
            while buff:
                nextItem = client.recv(1024)
                if nextItem.decode().endswith("end"):
                    buff += nextItem[0:len(nextItem) - 3]
                    break
                else:
                    buff += nextItem  
            print("Received File From Server")
            f = open(cmd_input.split(' ')[1], 'wb')
            f.write(buff)
            f.close()
            msg = buff.decode()
    elif cmd_input.split(' ')[0] == "store":
        fileName = cmd_input.split(' ')[1]
        if os.path.isfile(fileName):
            client.sendall(bytes(cmd_input, 'UTF-8'))
            with open(fileName, 'rb') as f:
                contents = f.read(1024)
                while contents:
                    client.send(contents)
                    contents = f.read(1024)
                print("File Stored on Server")
                client.send(bytes("end", "UTF-8"))
            f.close()
        else:
            print("Invalid file")
    elif cmd_input == "quit":
        client.sendall(bytes("quit",'UTF-8'))
        client.close()
        break
    else:
        print("Invalid command")
        print("Commands: list, retrieve <filename>, store <filename>, quit")
