# Audio Transcriptor
# This script will create the folder structure in the same manner as LJSpeech-1.1 dataset.
# This script will splitt the audio files on silenses and send the audio chunks to google recognition service
# Google will return the recognized text.
# This text will be writen to metadata.csv in the same manner as in LJSpeech-1.1 dataset.
# The audio chunks will also be saved in the same manner as in LJSpeech-1.1 dataset.

# This script must be in the same folder with audio files that should be transcripted
# The names of the audio files must be as follows: 01.mp3, 02.mp3, ..., 95.mp3 (or) 01.wav, 02.wav, ..., 95.wav

# To work with mp3-files you will need to install ffmpeg and put it to PATH.
# Windows instruction here http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/

# importing libraries 
import speech_recognition as sr 
import time
import os
from normalizer.normalizer import Normalizer # https://github.com/snakers4/russian_stt_text_normalization
import re

from pydub import AudioSegment 
from pydub.silence import split_on_silence
from pydub import AudioSegment, effects

# if you have many speakers, you can give each speaker an unique speaker id
Speaker_id = 'R001'

norm = Normalizer()

# a function that splits the audio file into chunks 
# and applies speech recognition 
def silence_based_conversion(path): 

	# open the audio file stored in the local system  
	#song = AudioSegment.from_wav(path) # <-- as a wav file
	song = AudioSegment.from_file(path, "mp3") # <-- as mp3 file

	# set the framerate of result autio
	song = song.set_frame_rate(16000)
		
	# split track where silence is 0.5 seconds or more and get chunks 
	chunks = split_on_silence(song, 
		# must be silent for at least 0.5 seconds 
		# or 500 ms. adjust this value based on user 
		# requirement. if the speaker stays silent for 
		# longer, increase this value. else, decrease it. 
		min_silence_len = 500, 

		# consider it silent if quieter than -36 dBFS 
		# adjust this per requirement 
		silence_thresh = -36
	) 

	# create a directory to store the metadata.csv. 
	try: 
		os.mkdir('LJSpeech-1.1') 
	except(FileExistsError): 
		pass

	# create a directory to store the audio chunks. 
	try: 
		os.mkdir('LJSpeech-1.1/wavs') 
	except(FileExistsError): 
		pass

	# open a file where we will concatenate and store the recognized text 
	fh = open("LJSpeech-1.1/metadata.csv", "a+", encoding="utf-8")
	
	# move into the directory to store the audio files. 
	os.chdir('LJSpeech-1.1/wavs') 

	
	# process each chunk 
	for chunk in chunks: 
		i = str(time.time()) # needed for unique filename
		i = i.replace('.','')

		# Create 1000 milliseconds silence chunk 
		# Silent chunks (1000ms) are needed for correct working google recognition
		chunk_silent = AudioSegment.silent(duration = 1000) 

		# Add silent chunk to beginning and end of audio chunk.
		# This is done so that it doesn't seem abruptly sliced. 
		# We will send this chunk to google recognition service
		audio_chunk_temp = chunk_silent + chunk + chunk_silent 

		# This chunk will be stored
		audio_chunk = chunk 

		# export audio chunk and save it in the current directory.
		# normalize the loudness in audio 
		audio_chunk = effects.normalize(audio_chunk)

		# specify the bitrate to be 192k
		# save audio file
		audio_chunk.export("./"+Speaker_id+"_{0}.wav".format(i), bitrate ='192k', format ="wav") 

		# save chunk for google recognition as temp.wav
		audio_chunk_temp.export("./temp.wav", bitrate ='192k', format ="wav") 

		# the name of the newly created chunk 
		filename = Speaker_id+'_'+str(i)
		print("Processing "+filename) 

		# get the name of the newly created chunk 
		# in the AUDIO_FILE variable for later use. 
		file = 'temp.wav'

		# create a speech recognition object 
		r = sr.Recognizer() 

		# recognize the chunk 
		with sr.AudioFile(file) as source: 
			# remove this if it is not working correctly. 
			r.adjust_for_ambient_noise(source) 
			audio_listened = r.listen(source) 

		try: 
			# try converting it to text 
			# if you use other language as russian, correct the language as described here https://cloud.google.com/speech-to-text/docs/languages
			rec = r.recognize_google(audio_listened, language="ru-RU").lower()

			# google recognition return numbers as integers i.e. "1, 200, 35".
			# text normalizer will read this numbers and return this as a writen russian text i.e. "один, двести, тридцать пять"
			# if you use other language as russian, repalce this line 
			rec = norm.norm_text(rec)

			# write the output to the metadata.csv.
			# in the same manner as in LJSpeech-1.1
			fh.write(filename+'|'+rec+'|'+rec+"\n") 

		# catch any errors. Audio files with errors will be not mentioned in metadata.csv
		except sr.UnknownValueError: 
			print("-- Could not understand audio") 

		except sr.RequestError as e: 
			print("--- Could not request results. check your internet connection") 

		# finaly remove the temp-file
		os.remove('./temp.wav')

	os.chdir('..')
	os.chdir('..') 

if __name__ == '__main__': 
	print('Start') 
	for k in range (1,96): 
		path = "{:02d}.mp3".format(k)
		print("{:02d}.mp3".format(k))
		try:
			open(path)
			silence_based_conversion(path) 
		except FileNotFoundError:
			print("File {} not found".format(path))


