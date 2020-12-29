import socket

HEADER_TCP = 20
HEADER_UDP = 8
PORT = 5010 #?
OUR_PORT = 2014
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname) # Should be 172.l.0.14
ADDR = (SERVER,PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    padded_send_len = b' ' * (HEADER_TCP-len(send_len))
    client.send(send_len)
    client.send(message)

send("Hello!")