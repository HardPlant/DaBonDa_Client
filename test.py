import RPi.GPIO as GPIO

from time import sleep

GPIO.setmode(GPIO.BOARD)
SOUND_LOW = 7
GPIO.setup(SOUND_LOW,GPIO.IN)
SOUND_EX = 5
GPIO.setup(SOUND_EX,GPIO.IN)
SOUND_HIGH = 21
GPIO.setup(SOUND_HIGH, GPIO.IN)

if __name__ == "__main__":
	try:
		low_queue = []
		high_queue = []
		while True:
			testcount = 0
			sound_low = GPIO.input(SOUND_LOW)
			sound_high = GPIO.input(SOUND_HIGH)
			sound_ex = GPIO.input(SOUND_EX)
			print(sound_low, sound_high, sound_ex)
			if len(low_queue) < 1024:
				low_queue.append(sound_low)
				high_queue.append(sound_high)

			else:
				break
			sleep(0.005)
		raise Exception


	except (KeyboardInterrupt, ValueError, Exception) as e:
		print(e)
		GPIO.cleanup()
