import logging
import time
import RPi.GPIO as GPIO

keyButtonBindings = {
	16: 'up',
	 6: 'left',
	12: 'right',
	13: 'down',
	26: 'return',
	20: 'del',
	19: 'escape'
}

def fun(pin):
	global last_input
	arrival_time = time.time()
	
	if pin not in keyButtonBindings.keys():
		print('Unknown button pin: {}'.format(pin))
	elif arrival_time-last_input>0.5:
		key = keyButtonBindings[pin]
		print('Sending {} as {}'.format(pin, key))
		last_input = arrival_time

if __name__=='__main__':
	GPIO.setmode(GPIO.BCM)
	for pin in keyButtonBindings.keys():
		GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.add_event_detect(pin, GPIO.RISING, callback=fun)

	try:
		last_input = time.time()
		while True:
			pass
	finally:
		GPIO.cleanup()
