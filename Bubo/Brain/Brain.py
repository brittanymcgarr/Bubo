################################################################################
## Brain                                                                      ##
## Bubo's Brain. Houses the Text to Speech and Speech to Text engines and     ##
## chooses responses based on enabled abilities.                              ##
################################################################################

import os
import json
import time
import datetime
import calendar

import speech_recognition as speech
from weather import Weather


class Brain:
    def __init__(self):
        self.recent_command = ""
        self.output = ""
        self.active = True

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
            command = recognizer.recognize_google(audio)
            self.recent_command = command.lower()
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
        elif "time" in self.recent_command:
            self.time_report()
            self.recent_command = ""
            self.speak()
        elif "sleep" in self.recent_command:
            self.active = False
            self.recent_command = "Goodnight"
            self.speak()

    def weather_report(self):
        weather = Weather()
        location = weather.lookup_by_location(self.city)
        forecasts = location.forecast()

        self.output = []
        self.output.append("Your three day weather forecast for " + self.city + " ")

        if not forecasts or len(forecasts) < 3:
            self.output.append("is not available at this time.")
            return

        today = datetime.datetime.now()

        for count in range(0, 3):
            date = today + datetime.timedelta(days=count)
            report = calendar.day_name[date.weekday()]
            report += " It will be " + forecasts[count].text()
            report += " with a low of " + forecasts[count].low()
            report += " and a high of " + forecasts[count].high()
            self.output.append(report)

    def time_report(self):
        time_string = time.strftime("%H:%M:%S")
        times = time_string.split(':')
        night = False

        if int(times[0]) > 12:
            times[0] = str(int(times[0]) - 12)
            night = True

        result = "The time is " + times[0] + " " + times[1]

        if night:
            result += "PM"
        else:
            result += "AM"

        self.output = [result]
