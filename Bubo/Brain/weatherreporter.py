################################################################################
## Weather                                                                    ##
## Weather skill for Bubo.                                                    ##
################################################################################

import datetime
import calendar

from weather import Weather


def weather_report(city):
    weather = Weather()
    location = weather.lookup_by_location(city)
    forecasts = location.forecast()

    output = ["Your three day weather forecast for {0}".format(city)]

    if not forecasts or len(forecasts) < 3:
        output.append("is not available at this time.")
        return

    today = datetime.datetime.now()

    for count in range(0, 3):
        date = today + datetime.timedelta(days=count)
        report = calendar.day_name[date.weekday()]
        report += "It will be {0}".format(forecasts[count].text())
        report += " with a low of {0}".format(str(forecasts[count].low()))
        report += " and a high of {0}".format(str(forecasts[count].high()))
        output.append(report)

    return output
