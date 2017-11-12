import requests,json, traceback

SERVER = "http://168.131.42.48:32772"
data = {"high" : '1', "low" : '1', "date" : '5', "image" : '3333'}
try:
	req = requests.post(url=SERVER+'/sound_data',json=json.dumps(data))
	print(req)
except Exception as e:
	traceback.print_exc(e)
