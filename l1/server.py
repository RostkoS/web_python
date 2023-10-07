# echo-server.py

import socket
import time

HOST = "127.0.0.1"  
PORT = 65432  
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()


       
while True:
            conn, addr = server.accept()
            print(f"Connected by {addr}")
            mesg = conn.recv(1024).decode('ascii')
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print(f"{mesg} - {current_time}")
