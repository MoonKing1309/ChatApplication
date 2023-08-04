import socket
import threading
import time

client = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
client.settimeout(0.2)
print("Connecting to Server")
while True:
    try:
        client.connect(('0.tcp.in.ngrok.io',13818))
    except:
        print("Trying to reach server...")
        time.sleep(5)
    else:
        while True:
            try:
                welcome = client.recv(1024).decode()
            except :
                pass
            else:
                print(welcome)
                client.send(input("Nickname : ").encode())
                break
        break


def receive():
    while True:
        try:
            msg = client.recv(4096).decode()
        except :
            continue
        else:
            print(msg,'\n->',end='')


def send():
    buffer=""
    while True:
        if(buffer!=""):
            client.send(buffer.encode())
            if('bye' in buffer.lower()):
                print("Connection Terminated")
                client.close()
                return
            buffer=""
        else:
            buffer = input("->->")
        
        
    
    
send_thread = threading.Thread(target=send)
receive_thread = threading.Thread(target=receive)
receive_thread.start()
send_thread.start()
