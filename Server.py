import socket
import threading
import time



SERVER = socket.gethostbyname(socket.gethostname()) # Should be 172.l.0.14
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
ALL_TIME_PLAYED = {}
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
    print("sending message")
    header = bytes.fromhex('feedbeef') + bytes.fromhex('02') + bytes.fromhex('07de')
    messageBytes = ("Server started, listening on IP address 169.254.135.241").encode(FORMAT)
    broadcast_message = header + messageBytes
    for i in range(10):
        broadcastServer.sendto(broadcast_message, ('<broadcast>', 13117))
        time.sleep(1)
    



def listen():
    TCPserver.listen()
    print (f"Server started, listening on IP address {SERVER}")
    conn, addr = TCPserver.accept()
    data = conn.recv(1024)
    print(data.decode(FORMAT))
    USERS_PER_GAME[addr[0]] = data.decode(FORMAT).split('\n')
    if(addr[0] not in ALL_TIME_PLAYED):
        ALL_TIME_PLAYED[addr[0]] = 0
    ALL_TIME_PLAYED[addr[0]] += 1
    time.sleep(10)
    conn.close()

def start():
    while True:
            thread = threading.Thread(target=listen)
            thread2 = threading.Thread(target=broadcast_message_before_game)
            thread.start()
            thread2.start()
            thread.join(10)
            thread2.join(10)
            if len(USERS_PER_GAME.keys()) > 0:
                print("game")
            else:
                print("No one joined the game")
            print(USERS_PER_GAME.keys())
            print("Game over, sending out offer requests...")
    
    
start()
