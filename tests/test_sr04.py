import time
import RPi.GPIO as GPIO
from threading import Thread

class GPIOThread(Thread):
	def __init__(self):
		Thread.__init__(self)
		self._running = True

	def running(self):
		return self._running

	def start(self):
		Thread.start(self)

	def stop(self):
		self._running = False

	def clean(self):
		GPIO.cleanup()

class GoalThread(GPIOThread):
	def __init__(self, parent, pin_trig, pin_echo):
		GPIOThread.__init__(self)
		self.parent = parent
		self.pin_trig = pin_trig
		self.pin_echo = pin_echo
		self.last_goal = time.time()

		GPIO.setmode(GPIO.BCM)
		GPIO.setup (self.pin_echo, GPIO.IN)
		GPIO.setup (self.pin_trig, GPIO.OUT)
		GPIO.output(self.pin_trig, GPIO.LOW)

	def run(self):
		try:
			# Waiting for sensor to settle
			time.sleep(2)

			while self.running():
				# Trigger a scan with a 10us pulse
				GPIO.output(self.pin_trig, GPIO.HIGH)
				time.sleep(0.00001)
				GPIO.output(self.pin_trig, GPIO.LOW)
				timeout = False
				start_read = time.time()

				# Read the echo
				while self.running() and GPIO.input(self.pin_echo)==0:
					pulse_start_time = time.time()
					# Prevent infinite loops, add timeout.
					if (time.time() - start_read) > 0.06:
						timeout = True
						break
				
				while self.running() and GPIO.input(self.pin_echo)==1:
					pulse_end_time = time.time()					
					# Prevent infinite loops, add timeout.
					if (time.time() - start_read) > 0.06:
						timeout = True
						break

				if self.running() and not timeout:
					pulse_duration = pulse_end_time - pulse_start_time
					distance = round(pulse_duration * 17150, 2)
					self._handle_dist(distance)
		finally:
			self.clean()

	def _handle_dist(self, dist):
		print('Distance: {}cm'.format(dist))
		if dist<10:
			if (time.time()-self.last_goal)>1:
				print('goal') #self.parent.goalDetected.emit(self.parent.side)
			
			self.last_goal = time.time()

if __name__=='__main__':
	try:
		_GoalPins = {
			'pin_trig': 3,
			'pin_echo': 2
		}
			
		goalThread = GoalThread(None, **_GoalPins)
		goalThread.start()
		
		while True:
			pass
			
	finally:
		goalThread.stop()
