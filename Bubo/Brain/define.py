################################################################################
## define_skill                                                               ##
## A skill for reading Wikipedia pages.                                       ##
################################################################################

import re
import wikipedia


def define(command):
    try:
        original = command.split()
        original.remove('define')
        subject = ' '.join(original)
    except ValueError:
        subject = command

    try:
        wiki = wikipedia.summary(subject, sentences=5)
        regex = re.compile(r'([^\(]*)\([^\)]*\) *(.*)')
        message = regex.match(wiki)

        while message:
            wiki = message.group(1) + message.group(2)
            message = regex.match(wiki)

        wiki = wiki.replace("'", "")
        output = [wiki]
    except wikipedia.exceptions.DisambiguationError as error:
        output = ["I could not find that definition. You may try: {0}".format(error)]

    return output
