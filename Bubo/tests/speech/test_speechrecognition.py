################################################################################
## Speech Recognition                                                         ##
## Quick module for testing installation of speech recognition module and     ##
## recording to .wav file for processing.                                     ##
################################################################################

import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak into the microphone")
    audio = recognizer.listen(source)

with open("../../transcripts/recording.wav", "wb") as recording:
    recording.write(audio.get_wav_data())

try:
    print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
