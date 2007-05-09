#!/usr/bin/python
import time

#This is a SMS function :: generic telephone number(with out nation code)+message
def sms(number,message):
	sdev=open('/dev/ttyS0','wb')
	sdev.write("at+cmgf=1\n\r")
	time.sleep(0.1)
	number='+1'+number
	sdev.write("at+cmgs=%s\n\r"%number)
	time.sleep(0.1)
	sdev.write(message)
	sdev.write("\x1A")
	time.sleep(0.1)
	sdev.close()

