import network
import socket
from time import *
from machine import Pin, ADC

#variables
reseau = 'Christophe'
mot_de_passe = 'alexZurcher'


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

# Transmission au serveur UDP
def send_UDP(val_capteur):
    UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPClientSocket.sendto(val_capteur.encode('UTF-8'), ("172.20.10.10", 12345))
    UDPClientSocket.close()


# Methode qui envoi toute les 5 secondes au serveur UDP la valeur POT
def detection_mouvement():
    pot = ADC(Pin(35))
    pot.atten(ADC.ATTN_11DB)       #Full range: 3.3v
    pot.width(ADC.WIDTH_12BIT)
    while True:
        # Print de la valeur du capteur 
        pot_value = pot.read()
        print(pot_value)
        # envoie en UDP
        send_UDP("salon/temp:"+str(pot_value))
        # stop 5 secondes
        sleep(2)


se_connecte() # 1. Connecter au Wifi

#angle=Angle() # 2. declaration de la variable pir de type pot

detection_mouvement() # 3. Lancer la detection de mouvement