from gpio import *
from time import *

pinLight=0 
pinLcd =1
pinAlarm =2
pinPush = 3
pinSpeaker = 4

def blink(v):
	pinMode(pinLight, OUT)
	customWrite(pinLight, int(v))
	
def alarmOn():
	pinMode(pinAlarm, OUT)
	digitalWrite(pinAlarm, HIGH)
	
def writeLcd(r):
	pinMode(pinLcd,OUT)
	customWrite(pinLcd, r)

def turnOffAlarm():
	pinMode(pinAlarm, OUT)
	digitalWrite(pinAlarm, LOW)

def clearAll():
	turnOffAlarm()
	blink(0)
	writeLcd("")
	makeSound(0)
	
		
def makeSound(v):
	print(v)
	if v > 1023:
		v = 1023
	elif(int(v) == 142):
		v = 0
	print(v)
	#analogWrite(pinSpeaker, v)


	
