# Audio-transcriptor-russian-
This script will split audio file on silence, transcript it with google recognition and save it in LJSpeech-1.1 dataset manner.
- This script will create the folder structure in the same manner as LJSpeech-1.1 dataset.
- This script will splitt the audio files on silenses and send the audio chunks to google recognition service
- Google will return the recognized text.
- Text normalization will change integers and text written with latin letters into russian text.
- Punctuation will set commas in text.
- This text will be writen to metadata.csv in the same manner as in LJSpeech-1.1 dataset.
- Audio chunks will be normalized on loudness.
- Audio chunks will also be saved in the same manner as in LJSpeech-1.1 dataset.
- See script for further description.

# requirements:
pydub

SpeechRecognition

torch --> for normalizer

tqdm --> for normalizer

pytorch_pretrained_bert==0.6.2 --> for punctuation (bert)

pymorphy2==0.8 --> for punctuation (bert)

to work with mp3-files you will need to install ffmpeg and put it to PATH. https://github.com/FFmpeg/FFmpeg Windows installation instruction here http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/

Text normalization from https://github.com/snakers4/russian_stt_text_normalization is implemented here. 

Punctuation (comma placement) from https://github.com/vlomme/Bert-Russian-punctuation dont forget to download pretrained model (see "how to use").

# how to use
- This script must be in the same folder with audio files that should be transcripted
- The names of the audio files must be as follows: 01.mp3, 02.mp3, ..., 99.mp3 (or) 01.wav, 02.wav, ..., 99.wav
- download pretrained bert model https://drive.google.com/file/d/190dLqhRjqgNJLKBqz0OxQ3TzxSm5Qbfx/view and place it in folder bert
- start the audio_transcribe.py in IDLE 

# how to optimize for your audio
- if you want to transcribe .wav-files instead of mp3 change

source_format = 'mp3' --> source_format = 'wav'

- if you want to remove chunks with strange symbol rate (text symbols per second audio), set

symbols_gate = True 

and set 

symbol_rate_min and symbol_rate_max

you can use it to separate one speaker speaking with special speaking speed, and/or poor transcriptions. You will also get additional information about rate and audio length in metadata.csv.

- if you want to remove chunks without speech, set

additional_clean = True

use it if you have audio with bad quality and chunks without speach.

- assign an Speaker_id

Speaker_id = 'R001_'

- change silence duration (in ms) for cut

min_silence_len = 500

- change silence value (in dBFS)

silence_thresh = -36

- change silense duration (in ms) to keep in audio

keep_silence = 100

- change audio framerate (in Hz) in result audio

frame_rate = 16000

- change length (in ms) of output audio file

target_length = 1000

- if you want to set commas in yout text:

punctuation = True

- if you want to use other language then russian:

change language in line

rec = r.recognize_google(audio_listened, language="ru-RU").lower() 

as discribed here https://cloud.google.com/speech-to-text/docs/languages

replace line

rec = norm.norm_text(rec)

and set

punctuation = False


# I wish you success
