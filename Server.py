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

#GAME TEXTS:
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
    



def listen(CONN_DICT,USERS_PER_GAME):
    TCPserver.listen()
    conn, addr = TCPserver.accept()
    CONN_DICT[addr[0]] = conn
    data = conn.recv(1024)
    print(data.decode(FORMAT))
    USERS_PER_GAME[addr[0]] = data.decode(FORMAT).split('\n')[0]
    
    

def start():
    print (f"Server started, listening on IP address {SERVER}")
    while True:     
            
                try:
                    USERS_PER_GAME = {} # {addr:Name}
                    CONN_DICT={}
                    thread = threading.Thread(target=listen,args = (CONN_DICT,USERS_PER_GAME))
                    thread2 = threading.Thread(target=broadcast_message_before_game)
                    thread.start()
                    thread2.start()
                    thread.join(10)
                    thread2.join(10)
                except:
                    print("Im here")
                    continue

                if(len(USERS_PER_GAME.keys()) > 0):
                    START_GAME_MESSAGE1 = "Welcome to Keyboard Spamming Battle Royale.\n"
                    START_GAME_MESSAGE2 = "Group 1:\n"
                    START_GAME_MESSAGE3 = "==\n"
                    START_GAME_MESSAGE4 = "Group 2:\n"
                    START_GAME_MESSAGE5 = "==\n"
                    START_GAME_MESSAGE6 = "Start pressing keys on your keyboard as fast as you can!!"
                    START_GAME_MESSAGE = START_GAME_MESSAGE1 + START_GAME_MESSAGE2 + START_GAME_MESSAGE3
                    
                    SCORES = {} #{ip:score}
                    GROUP1 = []
                    GROUP1SCORE = 0
                    GROUP2 = []
                    GROUP2SCORE = 0
                    
                    gamePlayersIp = sorted(list((USERS_PER_GAME.keys())))
                    for ipIndex in range (len(gamePlayersIp)//2):
                        ip = gamePlayersIp[ipIndex]
                        START_GAME_MESSAGE += str(USERS_PER_GAME[ip] + "\n")
                        SCORES[ip] = 0
                        GROUP1.append(ip)
            
                    START_GAME_MESSAGE += START_GAME_MESSAGE4 + START_GAME_MESSAGE5
            
                    for ipIndex in range (len(gamePlayersIp)//2,len(gamePlayersIp)):
                        ip = gamePlayersIp[ipIndex]
                        START_GAME_MESSAGE += str(USERS_PER_GAME[ip] + "\n")
                        SCORES[ip] = 0
                        GROUP2.append(ip)
                    
                    #GAME:
                    START_GAME_MESSAGE += START_GAME_MESSAGE6
                    try:
                        for ip_game in CONN_DICT.keys():
                            conn_player = CONN_DICT[ip_game]
                            conn_player.settimeout(30) #After that the server move on
                            thread_game = threading.Thread(target=game,args=(ip_game,conn_player,START_GAME_MESSAGE,SCORES))
                            thread_game.start()
                            thread.join(10)
                    except:
                        print("Times up")    
                    time.sleep(10)
                    #ENDGAME:
                    
                    for ip in SCORES:
                        if (ip in GROUP1):
                            GROUP1SCORE += SCORES[ip]
                        else:
                            GROUP2SCORE += SCORES[ip]
                        if(ip not in ALL_TIME_PLAYED.keys() or ALL_TIME_PLAYED [ip] < SCORES[ip]):
                            ALL_TIME_PLAYED [ip] = SCORES[ip]
                    if(GROUP1SCORE > GROUP2SCORE):
                        winnerGroup = "Group 1"
                    else:
                        winnerGroup = "Group 2"
                    
                    if(winnerGroup == "Group 1"):
                        winnerNameGroup = [x for x in USERS_PER_GAME if x in GROUP1]
                    else:
                        winnerNameGroup = [x for x in USERS_PER_GAME if x in GROUP2]
                    namesWinnerGroup = ""
                    for name in winnerNameGroup:
                        namesWinnerGroup += name + "\n"

                    END_GAME_MESSAGE = f"Game Over! Group 1 typed in {GROUP1SCORE} characters. Group 2 typed in {GROUP2SCORE} characters.\n {winnerGroup} wins!\n \n Congratulations to the winners:\n ==\n{namesWinnerGroup}"


                    for ip_game in CONN_DICT.keys():
                        conn_player = CONN_DICT[ip_game]
                        thread_endgame = threading.Thread(target=endgame,args=(ip_game,conn_player,END_GAME_MESSAGE))
                        thread_endgame.start()
                        thread.join()
                    print("Game over, sending out offer requests...")
                print("The All Time Leader is:")
                for ip in ALL_TIME_PLAYED:
                    if ALL_TIME_PLAYED[ip] == max(ALL_TIME_PLAYED.values()):
                        print(ip)
                        print(f"with score {ALL_TIME_PLAYED[ip]}")
                

def game(ip_game,conn_player,messageStart,SCORES):
        conn_player.send(messageStart.encode(FORMAT))
        try:
            while True:
                conn_player.recv(1024)
                SCORES[ip_game] += 1
        except:
            pass

        
def endgame(ip_game,conn_player,messagefinish):
        time.sleep(2)
        conn_player.send(messagefinish.encode(FORMAT))
        conn_player.close()           
    
    
start()


