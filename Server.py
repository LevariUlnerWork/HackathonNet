import socket
import threading

HEADER_TCP = 20
HEADER_UDP = 8
SERVER = socket.gethostbyname(socket.gethostname) # Should be 172.l.0.14
PORT = 5010 #?
OUR_PORT = 2014
ADDR = (SERVER,PORT) 
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_clients_before_game(conn, addr):
    print(f"Received offer from")


def start():
    server.listen()
    print (f"Server started, listening on IP address {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_clients_before_game, args=(conn,addr))
        thread.start()


start()