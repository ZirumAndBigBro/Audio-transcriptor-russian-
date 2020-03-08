# Audio-transcriptor-russian-
[Russian] This script will split audio file on silence, transcript it with google recognition and save it as in LJSpeech-1.1 dataset manner.
- This script will create the folder structure in the same manner as LJSpeech-1.1 dataset.
- This script will splitt the audio files on silenses and send the audio chunks to google recognition service
- Google will return the recognized text.
- This text will be writen to metadata.csv in the same manner as in LJSpeech-1.1 dataset.
- The audio chunks will also be saved in the same manner as in LJSpeech-1.1 dataset.


# requirements:
pip install pydub
pip install SpeechRecognition
to convert integers to text install https://github.com/Yuego/num2t4ru  put to your "\Python\Python36\Lib\site-packages" directory
to work with mp3-files you will need to install ffmpeg and put it to PATH. https://github.com/FFmpeg/FFmpeg Windows instruction here http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/

# how to use
- This script must be in the same folder with audio files that should be transcripted
- The names of the audio files must be as follows: 01.mp3, 02.mp3, ..., 95.mp3 (or) 01.wav, 02.wav, ..., 95.wav
- start the audio_transcribe.py in IDLE 

# how to optimize
- assign an Speaker_id if you want
- set other audio framerate in song = song.set_frame_rate(16000)
- set silence duration for cut min_silence_len = 500
- set silence value silence_thresh = -36

if you want to use other language as russian:
change 
rec = r.recognize_google(audio_listened, language="ru-RU").lower() 
as discribed here https://cloud.google.com/speech-to-text/docs/languages
replace 
rec = re.sub(r"(\d+)", lambda x: num2text(int(x.group(0))), rec)


I wish you success
