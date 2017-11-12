import RPi.GPIO as GPIO
from picamera import PiCamera
import datetime
import io
import base64
import requests
import json

from time import sleep

camera = PiCamera()

GPIO.setmode(GPIO.BOARD)
SOUND_LOW = 7
GPIO.setup(SOUND_LOW,GPIO.IN)

SOUND_HIGH = 21
GPIO.setup(SOUND_HIGH, GPIO.IN)

streamFile = io.BytesIO()
id = -1
SERVER = 'http://168.131.42.48:32772' 
url = SERVER + '/sound_data'

def getId():
	with open('id') as idFile:
		data = str(idFile.read())
	id = int(data)
	return id

def postRequest(data):
	global url
	body = json.dumps(data)
	print(body)
	resp = requests.post(url=url,json=body)
	print(resp)

def makeSoundData(id, low, high, image, date):
	image = len(image)
	return {
		'id' : id,
		'low' : low,
		'high' : high,
		'image' : image,
		'date' : date
	}

if __name__ == "__main__":
	id = getId()
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
				data = makeSoundData(id,low_count,high_count,b64,float_time)
				postRequest(data)

				low_queue.clear()
				high_queue.clear()
				streamFile.truncate(0)
				
			
			sleep(0.005)
		raise Exception


	except (KeyboardInterrupt, ValueError, Exception) as e:
		print(e)
		camera.stop_preview()
		GPIO.cleanup()
