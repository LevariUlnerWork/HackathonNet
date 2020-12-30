import socket
import threading
import time



SERVER = socket.gethostbyname(socket.gethostname) # Should be 172.l.0.14
BROADCAST_PORT = 13117
SERVER_PORT = 2014
ADDR = (SERVER,SERVER_PORT) 
FORMAT = 'utf-8'
diconnect_msg = "disconnect"

#The UDP Connections:
broadcastServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# Enable broadcasting mode
broadcastServer.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcastServer.settimeout(0.2)

#The TCP Connections:
TCPserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPserver.bind(ADDR)


#FOR THE GAME:
ALL_TIME_TABLE = {} # {Name:Score}
USERS_PER_GAME = {} # {addr:Name}
GROUP1 = {} # {Name:number of packets}
GROUP2 = {} # {Name:number of packets}

#GAME TEXTS:
START_GAME_MESSAGE1 = "Welcome to Keyboard Spamming Battle Royale."
START_GAME_MESSAGE2 = "Group 1:"
START_GAME_MESSAGE3 = "=="
START_GAME_MESSAGE4 = "Group 2:"
START_GAME_MESSAGE5 = "=="
START_GAME_MESSAGE6 = "Start pressing keys on your keyboard as fast as you can!!"
START_GAME_MESSAGE7 = "Game over!"
START_GAME_MESSAGE8 = "Group 1 typed in 104 characters. Group 2 typed in 28 characters."
START_GAME_MESSAGE9 = "Group 1 wins! \n"
START_GAME_MESSAGE10 = "Congratulations to the winners:"
START_GAME_MESSAGE11 = "=="





COLORS: {'Black': '\u001b[30m', \
'Red': '\u001b[31m' ,\
'Green': '\u001b[32m',\
'Yellow': '\u001b[33m',\
'Blue': '\u001b[34m',\
'Magenta': '\u001b[35m',\
'Cyan': '\u001b[36m',\
'White': '\u001b[37m',\
'Reset': '\u001b[0m}'}





def broadcast_message_before_game():
    header = bytes.fromhex('feedbeef') + bytes.fromhex('02') + bytes.fromhex('07de')
    messageBytes = ("Server started, listening on IP address 172.1.0.14").encode(FORMAT)
    broadcast_message = header + messageBytes
    for i in range(10):
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
    TCPserver.listen()
    print (f"Server started, listening on IP address {SERVER}")
    while True:
        conn, addr = TCPserver.accept()
        data, addr = TCPserver.recv(1024)
        USERS_PER_GAME[addr] = data.decode(FORMAT).split('\n')[0]
        thread = threading.Thread(target=broadcast_message_before_game, args=(conn,addr))
        thread.start()
        thread.join(10)

        print("Game over, sending out offer requests...")
    conn.close()

forever = True
while forever:
        start()
