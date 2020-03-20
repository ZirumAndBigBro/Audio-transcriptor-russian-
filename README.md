# Audio-transcriptor-russian-
This script will split audio file on silence, transcript it with google recognition and save it in LJSpeech-1.1 dataset manner.
- This script will create the folder structure in the same manner as LJSpeech-1.1 dataset.
- This script will splitt the audio files on silenses and send the audio chunks to google recognition service
- Google will return the recognized text.
- Text normalization will change integers and text written with latin letters into russian text. 
- This text will be writen to metadata.csv in the same manner as in LJSpeech-1.1 dataset.
- Audio chunks will be normalized on loudness.
- Audio chunks will also be saved in the same manner as in LJSpeech-1.1 dataset.
- See script for further description.

# requirements:
pip install pydub

pip install SpeechRecognition

pip install torch --> for normalizer

pip install tqdm --> for normalizer

to work with mp3-files you will need to install ffmpeg and put it to PATH. https://github.com/FFmpeg/FFmpeg Windows installation instruction here http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/

Text normalization from https://github.com/snakers4/russian_stt_text_normalization is implemented here. 

# how to use
- This script must be in the same folder with audio files that should be transcripted
- The names of the audio files must be as follows: 01.mp3, 02.mp3, ..., 99.mp3 (or) 01.wav, 02.wav, ..., 99.wav
- start the audio_transcribe.py in IDLE 

# how to optimize for your audio
- if you want to transcribe .wav-files instead of mp3 change

source_format = 'mp3' --> source_format = 'wav'

- assign an Speaker_id

Speaker_id = 'R001_'

- change silence duration (in ms) for cut

min_silence_len = 100

- change silence value (in dBFS)

silence_thresh = -36

- change silense duration (in ms) to keep in audio

keep_silence = 50

- change audio framerate (in Hz) in result audio

frame_rate = 16000

- change length (in ms) of output audio file

target_length = 4000

- if you want to use other language then russian:

change language in line

rec = r.recognize_google(audio_listened, language="ru-RU").lower() 

as discribed here https://cloud.google.com/speech-to-text/docs/languages

and replace line

rec = norm.norm_text(rec)


# I wish you success
