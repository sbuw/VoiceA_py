import vosk
import sys
import sounddevice as sd
import queue
import json

vosk.SetLogLevel(-1)
model = vosk.Model("model_small")
samplerate = 16000
device = 1

q = queue.Queue()

bActiveA = False

def q_callback(indata, frames, time, status):
	if status:
		print(status, file=sys.stderr)
	q.put(bytes(indata))

def va_listen(callback):
	with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
							channels=1, callback=q_callback):
		rec = vosk.KaldiRecognizer(model, samplerate)

		global bActiveA

		while bActiveA:
			data = q.get()
			if rec.AcceptWaveform(data):
				callback(json.loads(rec.Result())["text"])