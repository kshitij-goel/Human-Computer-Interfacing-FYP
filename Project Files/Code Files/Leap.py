import os, sys, inspect, math
from pubnub import Pubnub

src_dir=os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir='../lib/x64' if sys.maxsize>2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

pubnub=Pubnub(publish_key='pub-c-xxxx',subscribe_key='sub-c-xxxx')
#xxxx refer to unique keys which can be acquired for individual users. For safety purposes, these keys have been marked as xxxx

import Leap
from Leap import CircleGesture, SwipeGesture
def callback(message):
	print(message)

cl=0
councl=0
bck=0
fwd=0

class SampleListener(Leap.Listener):
	finger_names=['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
	bone_names=['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
	state_names=['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

def on_init(self, controller):
	print "Initialized"

def on_connect(self, controller):
	print "Connected"
	controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
	controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

def on_disconnect(self, controller):
	print "Disconnected"

def on_exit(self, controller):
	print "Exited"

def on_frame(self, controller):
	
	# Frame available
	frame=controller.frame()
	global cl
	global councl
	global bck
	global fwd
	
	# Get gestures
	for gesture in frame.gestures():
		if gesture.type==Leap.Gesture.TYPE_CIRCLE:
			circle=CircleGesture(gesture)
			
			# Determine clock direction using the angle between the pointable and the circle normal
			if circle.pointable.direction.angle_to(circle.normal)<=Leap.PI/2:
				clockwiseness="clockwise"
			else:
				clockwiseness="counterclockwise"
			if clockwiseness=="clockwise":
				cl=(cl+1)
				if cl==35:
					pubnub.publish('test', 'Turn Right', callback=callback, error=callback)
					cl=0
				else:
					councl=councl+1
					if councl==35:
						pubnub.publish('test', 'Turn Left', callback=callback, error=callback)
						councl=0
			if gesture.type==Leap.Gesture.TYPE_SWIPE:
				swipe=SwipeGesture(gesture)
				swdir=swipe.direction
				if (swdir.z>0 and math.fabs(swdir.z)>math.fabs(swdir.y) and math.fabs(swdir.z)>math.fabs(swdir.x)):
					bck=(bck+1)
					print "Move Backward"
					if bck==25:
						pubnub.publish('test', 'Move Backward', callback=callback, error=callback)
						bck=0
				elif (swdir.z<0 and math.fabs(swdir.z)>math.fabs(swdir.y) and math.fabs(swdir.z)>math.fabs(swdir.x)):
					fwd=(fwd+1)
					print "Move Forward"
					if fwd==25:
						pubnub.publish('test', 'Move Forward', callback=callback, error=callback)
						fwd=0

def state_string(self, state):
	if state==Leap.Gesture.STATE_START:
		return "STATE_START"
	if state==Leap.Gesture.STATE_UPDATE:
		return "STATE_UPDATE"
		if state==Leap.Gesture.STATE_STOP:
			return "STATE_STOP"
		if state==Leap.Gesture.STATE_INVALID:
			return "STATE_INVALID"

def main():
	# Create a sample listener and controller
	listener=SampleListener()
	controller=Leap.Controller()
	
	# Have the sample listener receive events from the controller
	controller.add_listener(listener)
	
	# Keep this process running until Enter is pressed
	print "Press Enter to quit..."
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		# Remove the sample listener when done
		pubnub.publish('test', 'Exit', callback=callback, error=callback)
		controller.remove_listener(listener)
		pubnub.unsubscribe(channel="test")

if __name__=="__main__":
	main()