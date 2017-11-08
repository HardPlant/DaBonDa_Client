import base64

input = input()
with open(input, "rb") as image_file:
	bytes = image_file.read()
	print(len(bytes))
	encoded_string = base64.b64encode(bytes)
	print(len(encoded_string))
