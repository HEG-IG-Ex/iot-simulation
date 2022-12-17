import paho.mqtt.client as mqtt #import the client1
import time
import keyboard
import socket



#Defining ip addresses
broker_address = "172.20.10.6"
broker_port = 1883

self_address = "172.20.10.4"
self_port = 12345

pkt_address = "172.20.10.3"
pkt_port = 1235


#MQTT
def on_publish(client,userdata,result):
    print("Data published over MQTT ! \n")
    pass

client1 = mqtt.Client("control1")
client1.on_publish = on_publish
client1.connect(broker_address, broker_port)
#ret = client1.publish("/test", "connecté")


#UDP Server
UDPServerSocket=socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((self_address, self_port))

while True:
    print("Le serveur UDP attend une connexion...")

    msgClient, coordClient=UDPServerSocket.recvfrom(1024)
    message_liste = msgClient.decode("UTF-8").split(":")
    
    mqtt_topic = message_liste[0]
    mqtt_value = message_liste[1]
    ret = client1.publish(mqtt_topic, mqtt_value)   

    UDPClientSocket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
    UDPClientSocket.sendto(msgClient,(pkt_address, pkt_port))

#Stopping UDP
print("Stopping UDP server socket")
UDPServerSocket.close()
client1.loop_stop()







    



