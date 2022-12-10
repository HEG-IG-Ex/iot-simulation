from realudp import *
from tcp import *
from time import *

IP_PKT_TCP_SERVER = "192.168.1.78"
PORT_PKT_TCP_SERVER = 1234

IP_VM_PERSON = "172.20.10.13" #"172.20.10.10"
PORT_VM_PERSON = 65535 #12345

tcp_client = TCPClient()

def onTCPConnectionChange(type):
	print("TCP : connection to " + tcp_client.remoteIP() + " changed to state " + str(type))

def onTCPReceive(data):
	print("TCP: received from " + tcp_client.remoteIP() + " with data: " + data)

def sendTCPmessage(data):
	tcp_client.send(data)

def onUDPReceive(ip, port, data):
	print("UDP : received from " + str(ip) + ":" + str(port) + " - Data: " + str(data))
	sendTCPmessage(data)
	
def startUDPServer():
	socket = RealUDPSocket()
	socket.onReceive(onUDPReceive)
	print("UDP Begin : " + str(socket.begin(1235)))
	
	tcp_client.onConnectionChange(onTCPConnectionChange)
	tcp_client.onReceive(onTCPReceive)
	print("TCP Begin : " + str(tcp_client.connect(IP_PKT_TCP_SERVER, PORT_PKT_TCP_SERVER)))
	
	count = 0	
	while True:
		count += 1
		sleep(3600)
	
	tcp_client.close()

if __name__ == "__main__":
	startUDPServer()