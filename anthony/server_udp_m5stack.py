import network
import socket
import time
from m5stack import lcd, speaker, buttonA, buttonB, buttonC

#Connecting to Wifi
network_wifi = 'iPhone AG'
password = 'Wifi_AG2121'
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

total_distance = 0

print("UDP server started")
while True:
    msg_client, coord_client = UDP_server_socket.recvfrom(1024)
    print("Message from client : ", msg_client.decode("UTF-8"))
    if msg_client.startswith("/salon"):
        msg_received = msg_client.decode("UTF-8").split(":")
        topic = msg_received[0]
        value_type_list = topic.split("/")
        room = value_type_list[1]
        value_type = value_type_list[2]
        value = msg_received[1]
    
        #M5 state depending on topic
        if value_type == "pot":
            lcd.println("Pot:", value)
        elif value_type == "pir":
            lcd.println("Présence dans: " + room)
        elif value_type == "ultra":
            value_float = float(value)
            lcd.println("Distance: " + value + " Sujet: " + value_type)
            total_distance = total_distance + abs(total_distance - value_float)
            lcd.println("Total: " + str(total_distance))
        elif value_type == "urgence":
            while not buttonA.isPressed():
                lcd.setTextColor(color=lcd.CYAN, bcolor=lcd.BLACK)
                speaker.volume(1)
                speaker.tone(freq=261, volume=1, duration=2)
                lcd.println("URGENCE ! au lieu: " + value)
                time.sleep(2)
    UDP_server_socket.sendto("Connected to UDP server".encode('UTF-8'), coord_client)
        
UDP_server_socket.close()