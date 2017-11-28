################################################################################
## Timekeeper                                                                 ##
## Timing skill set for Bubo.                                                 ##
################################################################################

import time


def time_report():
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

    return [result]
