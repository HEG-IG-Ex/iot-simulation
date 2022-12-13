from realudp import *
from tcp import *
from time import *
from lampe import *

IP_PKT_TCP_SERVER = "192.168.1.78"
PORT_PKT_TCP_SERVER = 1234

IP_VM_PERSON = "192.168.1.113"
PORT_VM_PERSON = 65535


tcp_client = TCPClient()
state = False

def onTCPConnectionChange(type):
	print("TCP : connection to " + tcp_client.remoteIP() + " changed to state " + str(type))

def onTCPReceive(data):
	print("TCP: received from " + tcp_client.remoteIP() + " with data: " + data)

def sendTCPmessage(data):
	tcp_client.send(data)

def onUDPReceive(ip, port, data):
	print("UDP : received from " + str(ip) + ":" + str(port) + " - Data: " + str(data))
	sendTCPmessage(data)
	value = data.split(":")[1]
	room = data.split(":")[0].split("/")[1]
	sensor = data.split(":")[0].split("/")[2]
	
	if(sensor == "pir"):
		blink(room, value)
		if(int(value) == 2):
			writeLcd(room)
		else:
			writeLcd("")
	
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