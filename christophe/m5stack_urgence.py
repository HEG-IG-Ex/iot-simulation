#dépendances
import network
import socket
from time import *
from machine import Pin
#import machine, time
from time import sleep

#M5Stack
from m5stack import *
lcd.font(lcd.FONT_Comic)
speaker.volume(2)
speaker.tone(freq=1800, duration=200)
lcd.text(80,100, 'Hello World')
print('Bonjour à tous')

#variables
reseau = 'Christophe'
mot_de_passe = 'alexZurcher'

# Methode pour la connexion au WiFi
def do_connect():
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

do_connect() # 1. Connecter au Wifi

#Bouton pour urgence
texte = "salon/temp:URGENCE"

#Méthode pour envoyer un message d'urgence si on presse sur le bouton
def on_wasPressed():
  lcd.print(texte)
  print(texte)
  send_UDP(texte)
  
buttonB.wasPressed(on_wasPressed)


     