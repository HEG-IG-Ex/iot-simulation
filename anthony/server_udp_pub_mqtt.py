import paho.mqtt.client as mqtt #import the client1
import time
import keyboard
import socket

#Defining ip addresses
broker_address = "10.177.38.120"
broker_port = 1883
self_address = "10.177.42.62"

#MQTT
def on_publish(client,userdata,result):
    print("Data published over MQTT ! \n")
    pass

client1 = mqtt.Client("control1")
client1.on_publish = on_publish
client1.connect(broker_address, broker_port)
ret = client1.publish("/test", 200) 

#UDP Server
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((self_address, 54321))
print("UDP server started")
while True:
    msgClient, coordClient = UDPServerSocket.recvfrom(1024)
    print("Message from client : ", msgClient.decode("UTF-8"))
    UDPServerSocket.sendto("Connected to UDP server".encode('UTF-8'), coordClient)
    ret = client1.publish("/test", msgClient.decode("UTF-8"))

#Stopping UDP
print("Stopping UDP server socket")
UDPServerSocket.close()