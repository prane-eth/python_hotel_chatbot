import speech_recognition as sr

# obtain path to "english.wav" in the same folder as this script
from os import path
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "test_voice.wav")
# .aiff and .flac formats supported


r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file


try:
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    print("You : " + r.recognize_google(audio))
except:
    print("could not understand audio")

# change default mic
import speech_recognition as sr;
print(str(sr.Microphone.list_microphone_names()))

#use
'''mic = sr.Microphone(device_index=3)'''
