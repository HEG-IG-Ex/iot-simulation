from tcp import *
from time import *
from realudp import *

port = 1234
server = TCPServer()
socket = RealUDPSocket()

def onUDPReceive(ip, port_received, data):
	print("received from "
		+ ip + ":" + str(port_received) + ":" + data);

def sendUDPMessage(data):
	socket.send("172.20.10.10", 12345, str(data))

def onTCPNewClient(client):
	def onTCPConnectionChange(type):
		print("connection to " + client.remoteIP() + " changed to state " + str(type))
		
	def onTCPReceive(data):
		print("received from " + client.remoteIP() + " with data: " + data)
		#sendUDPMessage(data)

	client.onConnectionChange(onTCPConnectionChange)
	client.onReceive(onTCPReceive)

def main():
	server.onNewClient(onTCPNewClient)
	print("TCP Begin : " + str(server.listen(port)))
	
	socket.onReceive(onUDPReceive)
	print("UDP Begin : " + str(socket.begin(12345)))

	# don't let it finish
	count = 0	
	while True:
		count += 1
		sleep(2000)

if __name__ == "__main__":
	main()