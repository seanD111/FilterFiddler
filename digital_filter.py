import numpy as np
import argparse
import sounddevice as sd
from scipy import signal


CABLE_DEVICES = ["CABLE Output (VB-Audio Virtual ", "Headphones (High Definition Aud"]
SAMPLERATE = 48000.0


if __name__ == "__main__":
	parser = argparse.ArgumentParser(add_help=False)

	dlti = signal.dlti([-1.1, 0+1j], [0.6+0.6j, 0.6-0.6j,-0.5], 3, dt=1/SAMPLERATE)
	def audio_callback(indata, outdata, frames, time, status):
		"""This is called (from a separate thread) for each audio block."""

		# zeros = np.ones((2, 1))*-1
		# poles = np.ones((2, 1))*0.9
		# gains = np.ones((2, 1))
		# dts = np.ones((2, 1)) *(1/SAMPLERATE)
		# Fancy indexing with mapping creates a (necessary!) copy:
		# _, outdata[:]= signal.dlsim((, 1/SAMPLERATE), indata[:])

		dt = frames*(1/SAMPLERATE)

		filtered_L = dlti.output(indata[:, 0], np.arange(0, dt, 1/SAMPLERATE), indata[0, 0])
		filtered_R = dlti.output(indata[:, 1], np.arange(0, dt, 1/SAMPLERATE), indata[0, 1])
		outdata[:, 0] = filtered_L[1][:, 0]
		outdata[:, 1] = filtered_R[1][:, 0]





	try:
		with sd.Stream(device=CABLE_DEVICES, callback=audio_callback):
			print('#' * 80)
			print('press Return to quit')
			print('#' * 80)
			input()
	except KeyboardInterrupt:
		parser.exit('')
	except Exception as e:
		parser.exit(type(e).__name__ + ': ' + str(e))
