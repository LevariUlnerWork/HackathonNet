import socket
import threading
import time



SERVER = socket.gethostbyname(socket.gethostname) # Should be 172.l.0.14
BROADCAST_PORT = 13117
SERVER_PORT = 2014
ADDR = (SERVER,SERVER_PORT) 
FORMAT = 'utf-8'
diconnect_msg = "disconnect"


#FOR THE GAME:
ALL_TIME_TABLE = {}
GROUP1 = {} # {addr:number of packets}
GROUP2 = {} # {addr:number of packets}



broadcastServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# Enable broadcasting mode
broadcastServer.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcastServer.settimeout(0.2)

TCPserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPserver.bind(ADDR)

def broadcast_message_before_game():
    header = bytes.fromhex('feedbeef') + bytes.fromhex('02') + bytes.fromhex('07de')
    messageBytes = ("Server started, listening on IP address 172.1.0.14").encode(FORMAT)
    broadcast_message = header + messageBytes
    while True:
        broadcastServer.sendto(broadcast_message, ('<broadcast>', 13117))
        time.sleep(1)
    

# def handle_clients_before_game(conn, addr):
#     print(f"new connection {addr} Received offer from")
#     connected = True
#     while connected:
#         msg_length = conn.recv(HEADER_UDP_MAGIC_COOKIE).decode(FORMAT)
#         if msg_length:
#             msg_length = int(msg_length)
#             msg = conn.recv(msg_length).decode(FORMAT)
#             if msg == diconnect_msg:
#                 connected = False
#             print(f"[{addr}] {msg}")
#             conn.send("msg recieved".encode(FORMAT))
#     conn.close()

def start():
    broadcastServer.listen()
    print (f"Server started, listening on IP address {SERVER}")
    while True:
        conn, addr = broadcastServer.accept()
        thread = threading.Thread(target=broadcast_message_before_game, args=(conn,addr))
        thread.start()
        thread.join(10)
    conn.close()

forever = True
while forever:
    isThereAreClients = False
    while not isThereAreClients:
        start()
