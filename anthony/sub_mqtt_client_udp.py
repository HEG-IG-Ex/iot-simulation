import paho.mqtt.client as mqtt #import the client1
import time
import keyboard
import socket

#
# Program description
#-------
#This program connects to the UDP server located on the M5 stack (IMAD)
#then it connects to the MQTT broker and subscribes to the required topics.
#
#When the programs recieves a MQTT message from the virtual machine on the other
#side of the MQTT broker, it sends it via UDP to the UDP server of the M5 stack


#Defining ip addresses
broker_address="172.20.10.4"
self_address="172.20.10.2"
udp_server_address="172.20.10.7"

def on_message(client, userdata, message):
    print("Message received : " ,str(message.payload.decode("utf-8")))
    print("Sending message: '" +  str(message.payload.decode("utf-8")) + "' over UDP")
    UDPClientSocket.sendto(message.payload, coordServer)

#Starting UDP client
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto("Client connected".encode('UTF-8'),(udp_server_address, 12345))
msgServer, coordServer = UDPClientSocket.recvfrom(1024)
print("(IP address, port) from server: ("+coordServer[0]+","+str(coordServer[1])+")")
print("Message from server: ", msgServer.decode("UTF-8"))

#Starting MQTT
print("Creating new instance")
client = mqtt.Client("client1")
client.on_message=on_message
print("Connecting to broker")
client.connect(broker_address)

#Starting MQTT subscriber
client.loop_start()
print("Subscribing to topic","/test")
client.subscribe("/test")

end = False
while end == False:
    if keyboard.is_pressed('q'):
        print('Program ending')
        end = True

#Stopping MQTT & UDP
print("Stopping MQTT")
client.loop_stop()
print("Closing UDP socket")
UDPClientSocket.close()