import socket

HEADER = 64
HOST = "127.0.0.1"  
PORT = 65432  

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
mesg = f'{input("")}'.encode('ascii')
mesg_len = len(mesg)
send_len = str(mesg_len).encode('ascii')
send_len += b' '*(HEADER - len(send_len))
client.send(send_len)
client.send(mesg)

response_len = client.recv(HEADER).decode('ascii')
response_len = int(response_len)
response = client.recv(response_len).decode('ascii')
         
print(f"{response}")