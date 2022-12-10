import paho.mqtt.client as mqtt #import the client1
import time
import keyboard
import socket

#Defining ip addresses
broker_address="10.177.38.120"
self_address="10.177.42.57"

def on_message(client, userdata, message):
    print("Message received : " ,str(message.payload.decode("utf-8")))
    print("Sending message: '" +  str(message.payload.decode("utf-8")) + "' over UDP")
    UDPClientSocket.sendto(message.payload, coordServer)

#Starting UDP client
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto("Client connected".encode('UTF-8'),("10.177.42.62", 12345))
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