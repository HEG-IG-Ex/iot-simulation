from gpio import *
from time import *

pinLight=0 

def blink(w):
	pinMode(pinLight, OUT)
	customWrite(pinLight, int(w))
	

