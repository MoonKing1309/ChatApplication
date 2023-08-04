import socket
import threading


server = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost',9999))
server.listen(5)
server.settimeout(0.5)

clients = dict()
print("WAITING FOR CLIENTS...")

def join(msg):
    for client in clients.keys():
        client.send(msg.encode())

def broadcast(msg,name):
    for client in clients.keys():
        client.send((name+':'+msg).encode())

def receive(client):
    while True:
        try:
            msg = client.recv(4096).decode()
        except :
            continue 
        else:
            print(clients[client] , ' : ' ,msg)
            broadcast(msg,clients[client])  
            if('bye' in msg.lower()):
                client.close()
                name = clients[client]
                clients.pop(client)
                join('\n->->' + name + 'has left the chat!')

        

def accept_conx():
    while True:
        try:
            client,address=server.accept()
        except:
            continue
        else:
            client.send("WELCOME! Please enter your nickname".encode())
            name = client.recv(1024).decode()
            clients[client] = name.upper()
            join(name.upper() + " has joined the chat!")
            threading.Thread(target = receive,args=(client,)).start()
            
        


accept_thread = threading.Thread(target=accept_conx)
accept_thread.start()


    