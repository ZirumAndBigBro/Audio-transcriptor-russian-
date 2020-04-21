# Audio Transcriptor
# This script will create the folder structure in the same manner as LJSpeech-1.1 dataset.
# This script will splitt the audio files on silenses and send the audio chunks to google recognition service
# Google will return the recognized text.
# This text will be writen to metadata.csv in the same manner as in LJSpeech-1.1 dataset.
# The audio chunks will also be saved in the same manner as in LJSpeech-1.1 dataset.

# This script must be in the same folder with audio files that should be transcripted
# The names of the audio files must be as follows: 01.mp3, 02.mp3, ..., 99.mp3 (or) 01.wav, 02.wav, ..., 99.wav

# To work with mp3-files you will need to install ffmpeg and put it to PATH.
# Windows instruction here http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/

# importing libraries 
import speech_recognition as sr 
import time
import os
import re
from normalizer.normalizer import Normalizer # https://github.com/snakers4/russian_stt_text_normalization
 
from pydub.silence import split_on_silence
from pydub import AudioSegment, effects

# Settings
source_format = 'mp3' # or 'wav' format of source audio file.
symbols_gate = True # only chunks with normal symbol rate (symbols per second) will be used
symbol_rate_min = 10 # min amount of symbols per second audio. if you use symbols_gate
symbol_rate_max = 20 # max amount of symbols per second audio if you use symbols_gate
additional_clean = True # before use chunk will be send to google cloud, if google can not recognize words in this chunk, it will be not used. True will consume additional time.
Speaker_id = 'R001_' # if you have many speakers, you can give each speaker an unique speaker id.
min_silence_len = 500 # silence duration for cut in ms. If the speaker stays silent for longer, increase this value. else, decrease it.
silence_thresh = -36 # consider it silent if quieter than -36 dBFS. Adjust this per requirement.
keep_silence = 100 # keep some ms of leading/trailing silence.
frame_rate = 16000 # set the framerate of result autio.
target_length = 1000 # target length of output audio files in ms.


norm = Normalizer()

# a function that splits the audio file into chunks 
# and applies speech recognition 
def silence_based_conversion(path): 

	# open the audio file stored in the local system
	if source_format == 'wav':
		song = AudioSegment.from_wav(path)
	else:
		song = AudioSegment.from_file(path, "mp3")

	# set the framerate of result autio
	song = song.set_frame_rate(frame_rate)
		
	# split track where silence is 0.5 seconds or more and get chunks 
	chunks = split_on_silence(song, min_silence_len, silence_thresh, keep_silence) 

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

	# additional clean. Use it if you want to remove chunks without speech.
	if additional_clean == True:
		checked_chunks = [chunks[0]]
		# check each chunk 
		for chunk in chunks: 

			# Create 1000 milliseconds silence chunk 
			# Silent chunks (1000ms) are needed for correct working google recognition
			chunk_silent = AudioSegment.silent(duration = 1000) 

			# Add silent chunk to beginning and end of audio chunk.
			# This is done so that it doesn't seem abruptly sliced. 
			# We will send this chunk to google recognition service
			audio_chunk_temp = chunk_silent + chunk + chunk_silent 

			# specify the bitrate to be 192k
			# save chunk for google recognition as temp.wav
			audio_chunk_temp.export("./check_temp.wav", bitrate ='192k', format ="wav") 

			# get the name of the newly created chunk 
			# in the AUDIO_FILE variable for later use. 
			file = 'check_temp.wav'

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
					checked_chunks.append(chunk)
					print("checking chunk - passed")
				except sr.UnknownValueError: 
					print("checking chunk - not passed") 

				except sr.RequestError as e: 
					print("--- Could not request results. check your internet connection") 
					# finaly remove the temp-file
			os.remove('./check_temp.wav')
		
		chunks = checked_chunks
        
	# now recombine the chunks so that the parts are at least "target_length" long
	output_chunks = [chunks[0]]
	for chunk in chunks[1:]:
		if len(output_chunks[-1]) < target_length:
			output_chunks[-1] += chunk
		else:
			output_chunks.append(chunk)

	chunks = output_chunks			

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
		# save chunk for google recognition as temp.wav
		audio_chunk_temp.export("./temp.wav", bitrate ='192k', format ="wav") 

		# the name of the newly created chunk 
		filename = Speaker_id+str(i)
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
			# text normalization will read this numbers and return this as a writen russian text i.e. "один, двести, тридцать пять"
			# if you use other language as russian, repalce this line 
			rec = norm.norm_text(rec)

			audio_length = float(len(audio_chunk))/1000 # audio length in seconds
			symbol_count = float(len(rec)) # text length in symbols

			if symbols_gate == True:
				if (symbol_count / audio_length > symbol_rate_min) and (symbol_count / audio_length < symbol_rate_max):
				
					print ("rate "+str(symbol_count/audio_length))	
					# write the output to the metadata.csv.
					# in the same manner as in LJSpeech-1.1
					fh.write(filename+'|'+rec+'|'+rec+"\n") 

					# save audio file
					audio_chunk.export("./"+Speaker_id+"{0}.wav".format(i), bitrate ='192k', format ="wav") 
					# catch any errors. Audio files with errors will be not mentioned in metadata.csv
				else: 
					print("- text too short or too long")
			else:
				# write the output to the metadata.csv.
				# in the same manner as in LJSpeech-1.1
				fh.write(filename+'|'+rec+'|'+rec+"\n") 

				# save audio file
				audio_chunk.export("./"+Speaker_id+"{0}.wav".format(i), bitrate ='192k', format ="wav") 
				# catch any errors. Audio files with errors will be not mentioned in metadata.csv

		except sr.UnknownValueError: 
			print("-- Could not understand audio") 

		except sr.RequestError as e: 
			print("--- Could not request results. Check your internet connection") 

		# finaly remove the temp-file
		os.remove('./temp.wav')

	os.chdir('..')
	os.chdir('..') 

if __name__ == '__main__': 
	print('Start') 
	for k in range (1,99): 
		path = "{:02d}.mp3".format(k)
		print("{:02d}.mp3".format(k))
		try:
			open(path)
			silence_based_conversion(path) 
		except FileNotFoundError:
			print("File {} not found".format(path))
