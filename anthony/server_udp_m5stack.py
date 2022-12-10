import network
import socket

#Pour la connection au Wifi
network: str = 'Christophe'
password: str = 'alexZurcher'

def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    
    if not sta_if.isconnected():
        print("Connecting to network...")
        sta_if.active(True)
        sta_if.connect(network, password)
        while not sta_if.isconnected():
            pass
        print("Network connected !", sta_if.ifconfig())
        
connect_wifi()

self_address: str = sta_if.ifconfig()[1]

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((self_address, 12345))

print("UDP server started")
while True:
    msgClient, coordClient = UDPServerSocket.recvfrom(1024)
    print("Message from client : ", msgClient.decode("UTF-8"))
    UDPServerSocket.sendto("Connected to UDP server".encode('UTF-8'), coordClient)
        
UDPServerSocket.close()