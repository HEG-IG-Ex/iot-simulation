from gpio import *
from time import *

pinLight=0 
pinLcd =1

def blink(r, v):
	pinMode(pinLight, OUT)
	customWrite(pinLight, int(v))
	
def writeLcd(r):
	pinMode(pinLcd,OUT)
	customWrite(pinLcd, r)
	
