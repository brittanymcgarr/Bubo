################################################################################
## Brain                                                                      ##
## Bubo's Brain. Houses the Text to Speech and Speech to Text engines and     ##
## chooses responses based on enabled abilities.                              ##
################################################################################

import os
import json

import speech_recognition as speech
from weather import Weather


class Brain:
    def __init__(self):
        self.recent_command = ""
        self.output = ""

        with open("profile/data.json") as file_data:
            profile = json.load(file_data)
            self.city = profile["city"]
            self.user = profile["user"]

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

        print(self.recent_command)

    def speak(self):
        if not self.output:
            return

        for output in self.output:
            os.system("espeak \"" + output + "\"")

        self.output = []

    def interpret(self):
        if self.recent_command == "":
            return

        if "weather" in self.recent_command:
            self.weather_report()
            self.recent_command = ""
            self.speak()

    def weather_report(self):
        weather = Weather()
        location = weather.lookup_by_location(self.city)
        forecasts = location.forecast()

        self.output = []
        self.output.append("Your three day weather forecast for " + self.city + " ")

        for forecast in forecasts[:3]:
            report = forecast.date()
            report += " It will be " + forecast.text()
            report += " with a low of " + forecast.low()
            report += " and a high of " + forecast.high()
            self.output.append(report)
