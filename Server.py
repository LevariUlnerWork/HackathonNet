import socket
import threading


HEADER_UDP_MAGIC_COOKIE = int('feedbeef',16)
MESSAGE_OFFER_TYPE = 2
SERVER = socket.gethostbyname(socket.gethostname) # Should be 172.l.0.14
BROADCAST_PORT = 13117
SERVER_PORT = 2014
ADDR = (SERVER,SERVER_PORT) 
FORMAT = 'utf-8'
diconnect_msg = "disconnect"

UDPserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
UDPserver.bind(ADDR)

def handle_clients_before_game(conn, addr):
    print(f"new connection {addr} Received offer from")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER_UDP_MAGIC_COOKIE).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == diconnect_msg:
                connected = False
            print(f"[{addr}] {msg}")
            conn.send("msg recieved".encode(FORMAT))
    conn.close()

def start():
    UDPserver.listen()
    print (f"Server started, listening on IP address {SERVER}")
    while True:
        conn, addr = UDPserver.accept()
        thread = threading.Thread(target=handle_clients_before_game, args=(conn,addr))
        thread.start()
        print(f"Active connction: {threading.activeCount()-1}")

print("Server started, listening on IP address * ")
start()
