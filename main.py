import config
import stt
import tts
from fuzzywuzzy import fuzz
import datetime
from num2t4ru import num2text
import webbrowser
import random
import os
import time
from sound import Sound

request_text = ''

def va_respond(voice: str):
	print(f"Я: "+voice)
	if voice.startswith(config.VA_ALIAS):
		# обращаются к ассистенту
		cmd = recognize_cmd(filter_cmd(voice))

		if cmd['cmd'] not in config.VA_CMD_LIST.keys():
			tts.va_speak(random.choice(config.VA_ANSWERS_IF_NOTH))
		else:
			execute_cmd(cmd['cmd'])


def filter_cmd(raw_voice: str):
	cmd = raw_voice

	for x in config.VA_ALIAS:
		cmd = cmd.replace(x, "").strip()

	for x in config.VA_TBR:
		cmd = cmd.replace(x, "").strip()

	global request_text
	request_text = cmd

	return cmd


def recognize_cmd(cmd: str):
	rc = {'cmd': '', 'percent': 0}
	for c, v in config.VA_CMD_LIST.items():

		for x in v:
			vrt = fuzz.ratio(cmd, x)
			if vrt > rc['percent']:
				rc['cmd'] = c
				rc['percent'] = vrt

	return rc


def execute_cmd(cmd: str):
	global request_text

	if cmd == 'help':
		# help
		text = "Я умею: ..."
		text += "произносить время ..."
		text += "рассказывать анекдоты ..."
		text += "включать радио ..."
		text += "открывать браузер, ютуб, вк ..."
		text += "включать и выключать звук ..."
		text += "и открывать браузер"
		tts.va_speak(text)
		pass
	elif cmd == 'ctime':
		# current time
		now = datetime.datetime.now()
		text = "Сейчас " + num2text(now.hour) + " " + num2text(now.minute)
		tts.va_speak(text)

	elif cmd == 'joke':
		jokes = ['Как смеются программисты? ... ехе ехе ехе',
					'ЭсКьюЭль запрос заходит в бар, подходит к двум столам и спрашивает .. «можно присоединиться?»',
					'Программист это машина для преобразования кофе в код']



		tts.va_speak(random.choice(jokes))

	elif cmd == 'open_browser':
		tts.va_speak("Открываю Браузер")
		webbrowser.open('www.google.com', new=1)

	elif cmd == 'open_vk':
		tts.va_speak("Открываю ВК")
		webbrowser.open('https://vk.com', new=1)

	elif cmd == 'open_yt':
		tts.va_speak("Открываю Ютуб")

		word = request_text.replace("ютуб", "")
		word = word.replace("включи", "")
		word = word.replace("открой", "")
		word = word.replace(" ", "+")

		if word != '+':
			webbrowser.open(f'https://www.youtube.com/results?search_query={word}', new=1)
		else:
			webbrowser.open(f'https://www.youtube.com/', new=1)

	elif cmd == 'radio':
		tts.va_speak("Включаю радио")
		webbrowser.open('https://www.youtube.com/watch?v=LtTtTG7ORLE', new=1)

	elif cmd == 'thanks':
		tts.va_speak(random.choice(config.VA_THANKS))

	elif cmd == 'search':
		tts.va_speak("Уже ищу")

		word = request_text.replace("найди", "")
		word = word.replace("отыщи", "")
		word = word.replace(" ", "+")

		webbrowser.open(f'https://www.google.com/search?q={word}', new=1)

	elif cmd == 'sound':
		s_int = 0

		c = request_text.split(' ')

		tts.va_speak("Выполняю")

		if c != None:
			for i in c:
				for j in config.VA_STR_INT.keys():
					if i == j:
						s_int += config.VA_STR_INT[j]
					else:
						pass

			Sound.volume_set(s_int)
		else:
			Sound.mute()

	elif cmd == 'hi':
		tts.va_speak(random.choice(config.VA_HELLO))

	elif cmd == 'how_are':
		tts.va_speak(random.choice(config.VA_HOW_ARE))

	#elif cmd == 'shutdown_pc':
	#	tts.va_speak('Выключаю компьютер')
	#	time.sleep(.5)
	#	os.system("shutdown /p")

# начать прослушивание команд
def startAssistent():
	print(f"{config.VA_NAME} (v{config.VA_VERSION}) начал свою работу ...")
	
	stt.va_listen(va_respond)