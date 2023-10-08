from ctypes import sizeof
import socket
import sys
import time

HEADER = 64
HOST = "127.0.0.1"  
PORT = 65432 
DISCONNECT_MESG = "DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()  

while True:
    print('Waiting for a connection...') 
    conn, addr = server.accept()
    print(f"Connected by {addr}")
    while True:
         mesg_len = conn.recv(HEADER).decode('ascii')
         if mesg_len != "":
           mesg_len = int(mesg_len)
           mesg = conn.recv(mesg_len).decode('ascii')
           if mesg == DISCONNECT_MESG:
            print("Connection closed")
            conn.close() 
            break
           else:
            t = time.localtime() 
            current_time = time.strftime("%H:%M:%S", t)
            print(f"{mesg} - {current_time}")
            time.sleep(5)
            b = conn.send(f"{mesg_len}".encode('ascii'))
            b = conn.send(f"{mesg}".encode('ascii'))
            
            