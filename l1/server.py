from ctypes import sizeof
import socket
import sys
import time

HEADER = 64
HOST = "127.0.0.1"  
PORT = 65432 
t = time.localtime() 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
     
while True:
            conn, addr = server.accept()
            print(f"Connected by {addr}")
            mesg_len = conn.recv(HEADER).decode('ascii')
            mesg_len = int(mesg_len)
            mesg = conn.recv(mesg_len).decode('ascii')
            current_time = time.strftime("%H:%M:%S", t)
            print(f"{mesg} - {current_time}")
            time.sleep(5)
            
            b = conn.send(f"{mesg_len}".encode('ascii'))
            b = conn.send(f"{mesg}".encode('ascii'))
            conn.close()
            print("Connection closed")