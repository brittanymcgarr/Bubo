################################################################################
## Text to Speech                                                             ##
## Reading the prompted string into audio format.                             ##
################################################################################

import os
import sys


def tts(message):
    if sys.platform == 'darwin':
        tts_engine = 'say'

        return os.system(tts_engine + '' + message)
    elif sys.platform == 'linux' or sys.platform == 'linux2':
        tts_engine = 'espeak'

        return os.system(tts_engine + ' "' + message + '"')


tts("Text to speech engine is working!")
