################################################################################
## Brain                                                                      ##
## Bubo's Brain. Houses the Text to Speech and Speech to Text engines and     ##
## chooses responses based on enabled abilities.                              ##
################################################################################

import os

import speech_recognition as speech


class Brain:
    def __init__(self):
        self.recent_command = ""
        print("Brain module loaded")

    def listen(self):
        recognizer = speech.Recognizer()

        with speech.Microphone() as source:
            audio = recognizer.listen(source)

        with open("transcripts/recent.wav", "wb") as recording:
            recording.write(audio.get_wav_data())

        try:
            self.recent_command = recognizer.recognize_google(audio)
        except speech.UnknownValueError:
            self.recent_command = "Unknown Error"
        except speech.RequestError:
            self.recent_command = "Request Error"

    def speak(self):
        if self.recent_command == "":
            return

        os.system("espeak \"" + self.recent_command + "\"")
        self.recent_command = ""
