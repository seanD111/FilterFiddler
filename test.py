import sounddevice as sd

for dev in sd.query_devices():
	print(dev)
print(sd.query_devices())

