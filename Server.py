import socket
import threading 
from scapy.all import *


HEADER_UDP_MAGIC_COOKIE = int('feedbeef',16)
MESSAGE_OFFER_TYPE = 2
SERVER = socket.gethostbyname(socket.gethostname) # Should be 172.l.0.14
BROADCAST_PORT = 13117
SERVER_PORT = 2014
ADDR = (SERVER,SERVER_PORT) 
FORMAT = 'utf-8'

UDPserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDPserver.bind(ADDR)

def handle_clients_before_game(conn, addr):
    print(f"Received offer from")


def start():
    UDPserver.listen()
    print (f"Server started, listening on IP address {SERVER}")
    while True:
        conn, addr = UDPserver.accept()
        thread = threading.Thread(target=handle_clients_before_game, args=(conn,addr))
        thread.start()


# start()
