import paho.mqtt.client as mqtt #import the client1
import time
import keyboard
import socket
import requests

#
# Program description
#-------
#This program connects to the UDP server located on the M5 stack (IMAD)
#then it connects to the MQTT broker and subscribes to the required topics.
#
#When the programs recieves a MQTT message from the virtual machine on the other
#side of the MQTT broker, it sends it via UDP to the UDP server of the M5 stack


#Defining ip addresse
broker_address="172.20.10.6"
self_address="172.20.10.14"
udp_server_address="172.20.10.5"

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = response.get("city")
    return location_data
#https://www.freecodecamp.org/news/how-to-get-location-information-of-ip-address-using-python
#Sources of this part of code above used to get the location of the device from the ip

def on_message(client, userdata, message):
    mqtt_message = message.payload.decode("utf-8")
    mqtt_topic = message.topic
    mqtt_all = mqtt_topic + ":" + mqtt_message
    print("Topic: ", mqtt_topic, "Message: ", mqtt_message, " au lieu: ", get_location())
    UDP_client_socket.sendto(mqtt_all.encode("utf-8"), coord_server)

#Starting UDP client
UDP_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDP_client_socket.sendto("UDP client connected".encode('UTF-8'),(udp_server_address, 12345))
msg_server, coord_server = UDP_client_socket.recvfrom(1024)
print("(IP address, port) from server: (" + coord_server[0] + "," + str(coord_server[1])+")")
print("Message from server: ", msg_server.decode("UTF-8"))

#Starting MQTT
print("Creating new instance")
client = mqtt.Client("client1")
client.on_message=on_message
print("Connecting to broker")
client.connect(broker_address)

#Starting MQTT subscriber and subbing to channels
client.loop_start()
print("Subscribing to different topics of","/salon")
client.subscribe("/salon/pot")
client.subscribe("/salon/pir")
client.subscribe("/salon/ultra")
client.subscribe("/salon/urgence")

end = False
while end == False:
    if keyboard.is_pressed('q'):
        print('Program ending')
        end = True

#Stopping MQTT & UDP
print("Stopping MQTT")
client.loop_stop()
print("Closing UDP socket")
UDP_client_socket.close()
