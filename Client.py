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

#Enable TCP connection:
client = None

def game():
    while True:
        key = msvcrt.getch()
        client.send(bytes(key))

while True:
    print("Client started, listening for offer requests... ")
    data, addr = clientUDP.recvfrom(1024)
    message = data[7:].decode(FORMAT)
    address = message.split('address ')[1]
    if((data[:5] == bytes.fromhex('feedbeef') + bytes.fromhex('02'))):
        dest_port = int.from_bytes(data[5:7],"big")
        SERVER_ADDR = (address,dest_port)
        print(f"Received offer from {address} , attempting to connect...")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(SERVER_ADDR)
        client.send("Gellers\n".encode(FORMAT))
        data, addr = client.recvfrom(100000)
        print(data.decode(FORMAT))
        try:
            thread_game = threading.Thread(target=game)
            thread_game.start()
            thread_game.join(10)
        except:
            print("Time is over!")
        data,addr = client.recvfrom(10000)
        print (data.decode(FORMAT))
        client.close()
        client = None
        print("Server disconnected, listening for offer requests...")
    



# send("Hello!")