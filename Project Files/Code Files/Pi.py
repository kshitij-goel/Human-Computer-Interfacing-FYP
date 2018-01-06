import sys,os
from time import sleep
import RPi.GPIO as GPIO
from pubnub import Pubnub

pubnub=Pubnub(publish_key='pub-c-xxxx',subscribe_key='sub-c-xxxx',ssl_on=False)
#The keys here should match the keys from the LeapMotion controller Python code

GPIO.setmode(GPIO.BOARD)

dir1=16
mtr1=12
dir2=15
mtr2=11

GPIO.setup(dir1,GPIO.OUT)
GPIO.setup(mtr1,GPIO.OUT)
GPIO.setup(dir2,GPIO.OUT)
GPIO.setup(mtr2,GPIO.OUT)

def _callback(message, channel):
	print (message +" - Pi")
	if message=="Move Backward":
		print "Backward"
		GPIO.output(dir1,1)
		GPIO.output(dir2,1)
		GPIO.output(mtr2,1)
		GPIO.output(mtr1,1)
		sleep(0.5)
		GPIO.output(dir1,1)
		GPIO.output(dir2,1)
		GPIO.output(mtr2,0)
		GPIO.output(mtr1,0)
	elif message=="Move Forward":
		print "Forward"
		GPIO.output(dir1,0)
		GPIO.output(dir2,0)
		GPIO.output(mtr2,1)
		GPIO.output(mtr1,1)
		sleep(0.5)
		GPIO.output(dir1,0)
		GPIO.output(dir2,0)
		GPIO.output(mtr2,0)
		GPIO.output(mtr1,0)
	elif message=="Turn Right":
		print "Turn Right"
		GPIO.output(dir1,0)
		GPIO.output(dir2,1)
		GPIO.output(mtr2,1)
		GPIO.output(mtr1,1)
		sleep(0.5)
		GPIO.output(dir1,0)
		GPIO.output(dir2,0)
		GPIO.output(mtr2,0)
		GPIO.output(mtr1,0)
	elif message=="Turn Left":
		print "Turn Left"
		GPIO.output(dir1,1)
		GPIO.output(dir2,0)
		GPIO.output(mtr2,1)
		GPIO.output(mtr1,1)
		sleep(0.5)
		GPIO.output(dir1,0)
		GPIO.output(dir2,0)
		GPIO.output(mtr2,0)
		GPIO.output(mtr1,0)
	elif message=="Exit":
		GPIO.cleanup()
		pubnub.unsubscribe(channel="test")
		os._exit(1)

def _error(message):
	print (message)

def _reconnect(message):
	print (message)

pubnub.subscribe(channels="test", callback=_callback, error=_error, reconnect=_reconnect)

try:
	while 1:
		pass
except KeyboardInterrupt:
	GPIO.cleanup()
	pubnub.unsubscribe(channel="test")