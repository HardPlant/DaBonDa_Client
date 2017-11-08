import RPi.GPIO as GPIO
from picamera import PiCamera
import datetime
import io
import base64

from time import sleep

camera = PiCamera()

GPIO.setmode(GPIO.BOARD)
SOUND_LOW = 7
GPIO.setup(SOUND_LOW,GPIO.IN)

SOUND_HIGH = 21
GPIO.setup(SOUND_HIGH, GPIO.IN)

streamFile = io.BytesIO()

if __name__ == "__main__":
	try:
		low_queue = []
		high_queue = []
		camera.start_preview()
		while True:
			sound_low = GPIO.input(SOUND_LOW)
			sound_high = GPIO.input(SOUND_HIGH)
			if len(low_queue) < 1024:
				low_queue.append(sound_low)
				high_queue.append(sound_high)

			else:
				low_count = low_queue.count(0)
				high_count = high_queue.count(0)
				float_time = datetime.datetime.now().timestamp()
				
				camera.capture(streamFile, 'jpeg', resize=(320,240), quality=30)
				b64 = base64.b64encode(streamFile.getbuffer())
				print(low_count, ",", high_count, len(b64))
				low_queue.clear()
				high_queue.clear()
				streamFile.truncate(0)
				
			
			sleep(0.005)
		raise Exception


	except (KeyboardInterrupt, ValueError, Exception) as e:
		print(e)
		camera.stop_preview()
		GPIO.cleanup()
