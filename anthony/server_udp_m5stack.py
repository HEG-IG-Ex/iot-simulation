import network
import socket
import time
import urequests
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
channel_list = ["Chaine 1: NRJ","Chaine 2: One FM", "Chaine 3: Virgin", "Chaine 4: Radio Plus", "Chaine 5: LFM", "Chaine 6: Sarrade FM", "Chaine 7: Bryce FM", "Chaine 8: Radio Lac", "Chaine 9: Rhone FM", "Chaine 10: BFM"]
print(self_address)

#Starting UDP server
UDP_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_server_socket.bind((self_address, 12345))

total_distance = 0

print("UDP server started")
while True:
    msg_client, coord_client = UDP_server_socket.recvfrom(1024)
    print("Message from client : ", msg_client.decode("UTF-8"))
    lcd.setTextColor(color=lcd.WHITE, bcolor=lcd.BLACK)
    if msg_client.startswith("/salon"):
        msg_received = msg_client.decode("UTF-8").split(":")
        topic = msg_received[0]
        value_type_list = topic.split("/")
        room = value_type_list[1]
        value_type = value_type_list[2]
        value = msg_received[1]
    
        #M5 state depending on topic
        if value_type == "pot":
            value_int = int(value) - 142
            if 0 <= value_int < 300:
                lcd.println(channel_list[0])
            elif 300 <= value_int < 600:
                lcd.println(channel_list[1])
            elif 600 <= value_int < 900:
                lcd.println(channel_list[2])
            elif 900 <= value_int < 1200:
                lcd.println(channel_list[3])
            elif 1200 <= value_int < 1500:
                lcd.println(channel_list[4])
            elif 1500 <= value_int < 1800:
                lcd.println(channel_list[5])
            elif 1800 <= value_int < 2100:
                lcd.println(channel_list[6])
            elif 2100 <= value_int < 2400:
                lcd.println(channel_list[7])
            elif 2400 <= value_int < 2700:
                lcd.println(channel_list[8])
            elif 2700 <= value_int < 3000:
                lcd.println(channel_list[9])
            else:
                lcd.println("Erreur dans les chaines")
            time.sleep(1)
        elif value_type == "pir":
            if int(value) == 0:
                lcd.print("Absence dans: " + room)
            elif int(value) == 1:
                lcd.print("Presence dans: " + room)
            else:
                lcd.print("Erreur de capteur infrarouge")
            time.sleep(2)
        elif value_type == "ultra":
            value_float = float(value)
            lcd.println("Distance actuelle: " + value)
            total_distance = total_distance + abs(total_distance - value_float)
            lcd.println("Distance totale: " + str(total_distance))
            time.sleep(4)
        elif value_type == "urgence":
            while not buttonA.isPressed():
                lcd.setTextColor(color=lcd.CYAN, bcolor=lcd.BLACK)
                speaker.volume(1)
                speaker.tone(freq=261, volume=1, duration=2)
                lcd.println("URGENCE ! au lieu: " + value)
                time.sleep(4)
        lcd.clear()
        lcd.setCursor(0,100)
    UDP_server_socket.sendto("Connected to UDP server".encode('UTF-8'), coord_client)
        
UDP_server_socket.close()