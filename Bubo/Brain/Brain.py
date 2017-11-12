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
import re

import speech_recognition as speech
from weather import Weather
import wikipedia


class Brain:
    def __init__(self):
        self.recent_command = ""
        self.output = ""
        self.active = True
        self.state = 'LISTEN'

        with open("profile/data.json") as file_data:
            profile = json.load(file_data)
            self.city = profile["city"]
            self.user = profile["user"]

        print("Brain module loaded")

    def listen(self):
        if not self.state == 'LISTEN':
            return

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

        self.state = 'COMMAND'
        keywords = set(self.recent_command.split(' '))

        names = ["bibo", "bebo", "bubo", "fubo",
                 "bhutto", "bebo", "boohbah"]
        names = set(names)

        if not names.intersection(keywords):
            self.state = 'LISTEN'
            return

        command = self.recent_command.split()
        command = [word for word in command if word not in names]
        self.recent_command = ' '.join(command)

        if "weather" in keywords:
            self.weather_report()
        elif "time" in keywords:
            self.time_report()
        elif "define" in keywords:
            self.define()
        elif "sleep" in keywords:
            self.active = False
            self.output = ["Goodnight"]
            self.speak()
            return

        self.speak()
        self.recent_command = ""
        self.state = 'LISTEN'
        return

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

    def define(self):
        try:
            original = self.recent_command.split()
            original.remove('define')
            subject = ' '.join(original)
        except ValueError:
            subject = self.recent_command

        try:
            wiki = wikipedia.summary(subject, sentences=5)
            regex = re.compile(r'([^\(]*)\([^\)]*\) *(.*)')
            message = regex.match(wiki)

            while message:
                wiki = message.group(1) + message.group(2)
                message = regex.match(wiki)

            wiki = wiki.replace("'", "")
            self.output = [wiki]
        except wikipedia.exceptions.DisambiguationError as error:
            self.output = ["I could not find that definition. You may try: {0}".format(error)]
