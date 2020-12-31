import socket
import threading
import time
import os



SERVER = socket.gethostbyname("172.1.0.14") # Should be 172.l.0.14 - Our hostname
BROADCAST_PORT = 13117
SERVER_PORT = 2014 #ours
ADDR = (SERVER,SERVER_PORT) 
FORMAT = 'utf-8'


#The UDP Connections:
broadcastServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# Enable broadcasting mode
broadcastServer.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcastServer.settimeout(0.2)

#The TCP Connections:
TCPserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPserver.bind(ADDR)


#FOR THE GAME:
ALL_TIME_PLAYED = {} # {Name:Score}
MOST_FREQ_KEY = {} #{key:Freq ever}

#SET SCREEN:
os.system("cls")
COLORS = {'Black': '\u001b[30m', \
'Red': '\u001b[31m' ,\
'Green': '\u001b[32m',\
'Yellow': '\u001b[33m',\
'Blue': '\u001b[34m',\
'Magenta': '\u001b[35m',\
'Cyan': '\u001b[36m',\
'White': '\u001b[37m',\
'Reset': '\u001b[0m'}





def broadcast_message_before_game():
    header = bytes.fromhex('feedbeef') + bytes.fromhex('02') + bytes.fromhex('07de')
    messageBytes = ("Server started, listening on IP address 169.254.135.241").encode(FORMAT)
    broadcast_message = header + messageBytes
    for i in range(10):
        broadcastServer.sendto(broadcast_message, ('<broadcast>', 13117))
        time.sleep(1)
    



def listen(CONN_DICT,USERS_PER_GAME):
    startTime = time.time()
    while startTime + 10 > time.time():
        TCPserver.listen()
        conn, addr = TCPserver.accept()
        data = conn.recv(1024)
        playerName = data.decode(FORMAT).split('\n')[0]
        CONN_DICT[playerName] = conn
        USERS_PER_GAME[playerName] = addr[0] 
        
    

def start():
    print (f"Server started, listening on IP address {SERVER}")
    
    while True:            
        try:
            
            USERS_PER_GAME = {} # {Name: ip}
            CONN_DICT={} #{name : connection per game}
            
            thread = threading.Thread(target=listen,args = (CONN_DICT,USERS_PER_GAME)) #thread per tcp start connection
            thread2 = threading.Thread(target=broadcast_message_before_game) #thread per broadcasts
            thread.start()
            thread2.start()
            thread.join(10)
            thread2.join(10)
        except Exception as e:
            print("connection lost")
            continue


        #Enter the game:
        if(len(USERS_PER_GAME.keys()) > 0):
            
            #Building the game:
            SCORES = {} #{Name:score}
            GROUP1 = []
            GROUP1SCORE = 0
            GROUP2 = []
            GROUP2SCORE = 0
            
            #Build the message:
            START_GAME_MESSAGE1 = "Welcome to Keyboard Spamming Battle Royale.\n"
            START_GAME_MESSAGE2 = "Group 1:\n"
            START_GAME_MESSAGE3 = "==\n"
            START_GAME_MESSAGE4 = "Group 2:\n"
            START_GAME_MESSAGE5 = "==\n"
            START_GAME_MESSAGE6 = "Start pressing keys on your keyboard as fast as you can!!"
            START_GAME_MESSAGE = START_GAME_MESSAGE1 + START_GAME_MESSAGE2 + START_GAME_MESSAGE3
            
            
            gamePlayersName = sorted(list((USERS_PER_GAME.keys())))
            for NameIndex in range (len(gamePlayersName)//2):
                name = gamePlayersName[NameIndex]
                START_GAME_MESSAGE += str(name + "\n")
                SCORES[name] = 0
                GROUP1.append(name)
    
            START_GAME_MESSAGE += START_GAME_MESSAGE4 + START_GAME_MESSAGE5
            for NameIndex in range (len(gamePlayersName)//2,len(gamePlayersName)):
                name = gamePlayersName[NameIndex]
                START_GAME_MESSAGE += str(name + "\n")
                SCORES[name] = 0
                GROUP1.append(name)
            
            START_GAME_MESSAGE += START_GAME_MESSAGE6
            print (COLORS["Magenta"] + START_GAME_MESSAGE)

            #GAME:
                
            for name in CONN_DICT.keys():
                #Get any user connection:
                conn_player = CONN_DICT[name]
                conn_player.settimeout(30) #After that the server move on - raise a time out exception
                
                #thread per user:
                thread_game = threading.Thread(target=game,args=(name,conn_player,START_GAME_MESSAGE,SCORES))
                thread_game.start()
                thread_game.join(10)
            print(COLORS["Red"] + "Times up!")    
            
            time.sleep(2)
            
            #ENDGAME (you obviously understood the reference):
            
            #calculate the scores and save them forever:
            for name in SCORES:
                if (name in GROUP1):
                    GROUP1SCORE += SCORES[name]
                else:
                    GROUP2SCORE += SCORES[name]
                
                #Record this player
                if(name not in ALL_TIME_PLAYED.keys() or ALL_TIME_PLAYED [name] < SCORES[name]):
                    ALL_TIME_PLAYED [name] = SCORES[name]
            
            #Decide the winners:
            if(GROUP1SCORE > GROUP2SCORE):
                winnerGroup = "Group 1"
            else:
                winnerGroup = "Group 2"
            
            if(winnerGroup == "Group 1"):
                winnerNameGroup = [x for x in USERS_PER_GAME.keys() if x in GROUP1]
            else:
                winnerNameGroup = [x for x in USERS_PER_GAME.keys() if x in GROUP2]
            
            namesWinnerGroup = ""
            for name in winnerNameGroup:
                namesWinnerGroup += name + "\n"

            END_GAME_MESSAGE = f"Game Over! Group 1 typed in {GROUP1SCORE} characters. Group 2 typed in {GROUP2SCORE} characters.\n{winnerGroup} wins!\n \nCongratulations to the winners:\n ==\n{namesWinnerGroup}"

            #Send the end message:
            print(COLORS["Blue"]+END_GAME_MESSAGE)
            for name in CONN_DICT.keys():
                conn_player = CONN_DICT[name]
                thread_endgame = threading.Thread(target=endgame,args=(name,conn_player,END_GAME_MESSAGE))
                thread_endgame.start()
                thread.join(1)
            print(COLORS["Reset"]+"Game over, sending out offer requests...")
        else:
            print(COLORS["Reset"]+"No game, sending out offer requests...")
        print("The All Time Leaders are:")
        best_score = 0
        for ip in ALL_TIME_PLAYED:
            if ALL_TIME_PLAYED[ip] == max(ALL_TIME_PLAYED.values()):
                print(ip)
                best_score = ALL_TIME_PLAYED[ip] 
        print(f"with score {best_score}")

        print(f"The most common keys are:")
        key_score = 0
        for key in MOST_FREQ_KEY:
            if MOST_FREQ_KEY[key] == max(MOST_FREQ_KEY.values()):
                print(key)       
                key_score = MOST_FREQ_KEY[key] 
        print(f"they were sent: {key_score} times!")
                

def game(name,conn_player,messageStart,SCORES):
    try:
        #Start Game Message:
        conn_player.send(messageStart.encode(FORMAT))

        start_game_time = time.time()
        while start_game_time + 10 > time.time():
            data,addr = conn_player.recvfrom(1024)
            key = data.decode(FORMAT)
            if(key not in MOST_FREQ_KEY.keys()):
                MOST_FREQ_KEY[key] = 0
            MOST_FREQ_KEY[key] += 1
            SCORES[name] += 1
    except:
        pass

        
def endgame(name, conn_player, messagefinish):
    try:
        conn_player.send(messagefinish.encode(FORMAT))
        print (f"Connection with {name} close")
        conn_player.close()
    except:
        pass
    
    
start()


