import socket

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


#Enable TCP connection:
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


clientUDP.bind(("", 13117))
while True:
    print("Client started, listening for offer requests... ")
    data, addr = clientUDP.recvfrom(1024)
    message = data[7:].decode(FORMAT)
    address = message.split('address ')[1]
    if((data[:5] == bytes.fromhex('feedbeef') + bytes.fromhex('02'))):
        dest_port = int.from_bytes(data[5:7],"big")
        SERVER_ADDR = (address,dest_port)
        print(f"Received offer from {address} , attempting to connect...")
        client.connect(SERVER_ADDR)
        client.send("Gellers\n".encode(FORMAT))
        client.listen()
        break



def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER_TCP-len(send_len))
    client.send(send_len)
    client.send(message)

# send("Hello!")