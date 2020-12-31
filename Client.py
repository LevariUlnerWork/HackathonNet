import time
import socket
import threading
import msvcrt

HEADER_TCP = 20
HEADER_UDP = 8
SERVER_PORT = 0
PORT = 0
SERVER_ADDR = 0
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname()) # Should be 172.l.0.14
ADDR = (SERVER,PORT)
diconnect_msg = "disconnect"


clientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
clientUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Enable broadcasting mode
clientUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
clientUDP.bind(("", 13117))


def start():
    while True:
        #Broadcast:
        print("Client started, listening for offer requests... ")
        data, addr = clientUDP.recvfrom(1024)
        header = data[:5]
        message = data[7:].decode(FORMAT) #The message
        address = message.split('address ')[1]
        
        #Check the message format:
        if header == bytes.fromhex('feedbeef') + bytes.fromhex('02'):
            
            dest_port = int.from_bytes(data[5:7],"big")
            SERVER_ADDR = (address,dest_port)
            
            print(f"Received offer from {address} , attempting to connect...")
            
            #Enable TCP connection:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(SERVER_ADDR)
            client.send("Gellers\n".encode(FORMAT))
            
            #Game starts:
            data, addr = client.recvfrom(100000)
            print(data.decode(FORMAT))

            def game():
                while True:
                    try:
                        key = msvcrt.getch()
                        client.send(key)
                    except Exception as e:
                        print (e)
                        pass            
            
            try:
                e = threading.Event()
                
                t = threading.Thread(target=game,args=())
                t.start()
                t.join(10)
                
                #Times up!
                if(t.is_alive()):
                    e.set()
                    print("Time's Up!")
                
            except Exception as e:
                print("Time's Up!")
                pass
            
            #EndGame:
            data,addr = client.recvfrom(10000)
            print (data.decode(FORMAT))
            client = None
            
            print("Server disconnected, listening for offer requests...")
    


start()


# send("Hello!")