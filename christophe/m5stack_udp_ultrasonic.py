# dépendances
import network
import socket
from time import *
from machine import Pin
import machine, time
from time import sleep

#variables
reseau = 'Christophe'
mot_de_passe = 'alexZurcher'

# Definir la class Ultrason
class UltraSon:
 def __init__(self, pinTrig, pinEcho):
     self.timeout = 1000000
     self.trigger = Pin(pinTrig, Pin.OUT)
     self.echo = Pin(pinEcho, Pin.IN)
     self.trigger.value(0)
     
 def mesure(self):
     self.trigger.value(0)
     time.sleep_us(2)
     self.trigger.value(1)
     time.sleep_us(10)
     self.trigger.value(0)
     duree = machine.time_pulse_us(self.echo, 1, self.timeout)
     distance=duree*0.017
     return distance

# Methode pour la connexion au WiFi
def se_connecte():
    sta_if = network.WLAN(network.STA_IF)

    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(reseau, mot_de_passe)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

# Transmission UDP
def send_UDP(val_capteur):
    UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPClientSocket.sendto(val_capteur.encode('UTF-8'), ("172.20.10.10", 12345))
    UDPClientSocket.close()


# Methode qui envoie toute les 5 secondes au serveur UDP la valeur Ultrasonic
def detection_mouvement():
    while True:
        # Print de la valeur du capteur {0,1}
        print(ultra.mesure())

        send_UDP("salon/temp:"+str(ultra.mesure())) # envoie en UDP

        # stop 5 secondes
        sleep(5)

se_connecte() # 1. Connecter au Wifi

ultra=UltraSon(21,22) # 2. declaration de la variable pir de type Ultrason

detection_mouvement() # 3. Lancer la detection de mouvement
