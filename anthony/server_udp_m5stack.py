import network
import socket

#Connecting to Wifi
network_wifi = 'Christophe'
password = 'alexZurcher'
sta_if = network.WLAN(network.STA_IF)

def connect_wifi():
    if not sta_if.isconnected():
        print("Connecting to network...")
        sta_if.active(True)
        sta_if.connect(network_wifi, password)
        while not sta_if.isconnected():
            pass
        print("Network connected !", sta_if.ifconfig())
        
connect_wifi()

self_address = sta_if.ifconfig()[0]

print(self_address)

#Starting UDP server
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPServerSocket.bind((self_address, 12345))

print("UDP server started")
while True:
    msgClient, coordClient = UDPServerSocket.recvfrom(1024)
    print("Message from client : ", msgClient.decode("UTF-8"))
    UDPServerSocket.sendto("Connected to UDP server".encode('UTF-8'), coordClient)
        
UDPServerSocket.close()