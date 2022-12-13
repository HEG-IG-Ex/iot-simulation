import network
import socket
import time
from m5stack import lcd, speaker, buttonA, buttonB, buttonC

#Connecting to Wifi
network_wifi = ''
password = ''
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
UDP_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_server_socket.bind((self_address, 12345))

print("UDP server started")
while True:
    msg_client, coord_client = UDP_server_socket.recvfrom(1024)
    print("Message from client : ", msg_client.decode("UTF-8"))
    if msg_client.startswith("/salon"):
        msg_received = msg_client.decode("UTF-8").split(":")
        topic = msg_received[0]
        value = msg_received[1]
    
        #M5 state depending on topic
        if topic == "/salon/pot":
            print("Pot:", value)
        elif topic == "/salon/pir":
            print("Pir:", value)
        elif topic == "/salon/ultra":
            print("Ultra:", value)
        elif topic == "/salon/urgence":
            while not buttonA.isPressed():
                speaker.volume(1)
                speaker.tone(freq=1800,duration=1)
                lcd.setTextColor(color=lcd.CYAN, bcolor=lcd.WHITE)
                lcd.print("URGENCE !\n")
    UDP_server_socket.sendto("Connected to UDP server".encode('UTF-8'), coord_client)
        
UDP_server_socket.close()