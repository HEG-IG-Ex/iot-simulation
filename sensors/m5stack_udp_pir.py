import network
import socket
from time import *
from machine import Pin

reseau = 'xxx'
mot_de_passe = 'xxx'

vm_ip = "172.20.10.4"
vm_port = 12345

# Definir la class PIR
class PIR():
    def __init__(self):
        self.pin = Pin(22,Pin.IN)
        self.mvt = 0
        self.pin.irq(trigger=(Pin.IRQ_RISING | Pin.IRQ_FALLING),handler=self.actionInterruption)

    def actionInterruption(self,pin):
        if (pin.value()==1):
            if (self.mvt==0):
                self.mvt=1
        else:
            if (self.mvt==1):
                self.mvt=0

    def read(self):
        return self.mvt

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
    UDPClientSocket.sendto(val_capteur.encode('UTF-8'), (vm_ip, vm_port))
    UDPClientSocket.close()

# Methode qui envoi toute les 5 secondes au serveur la valeur du PIR
def detection_mouvement():
    while True:
        # Print de la valeur du capteur {0,1}
        print(pir.read())
        # transmission UDP
        send_UDP("/salon/pir:"+str(pir.read())) 
        # stop 5 secondes
        sleep(5)


se_connecte() # 1. Connecter au Wifi

pir=PIR() # 2. declaration de la variable pir de type PIR

detection_mouvement() # 3. Lancer la detection de mouvement
