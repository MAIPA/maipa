# MAIPA
################################################################################
import os
import sys
import json
import time
import random
import speech_recognition as sr

from ctypes import *
################################################################################
def error_supress():
    #suppression for ALSA audio errors
    ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
def py_error_handler(filename, line, function, err, fmt):
    pass
################################################################################
def say_response(said):
    #ideally send to API server to get a response at this point
    if said == "":
        pass
    elif said in ('hello' or 'hi' or 'whats up'):
        print "Heya, how's it going?"
        tts("Heya, how's it going?")
    elif said in ('how are you' or 'how are you doing'):
        print "I am still functioning as intended, thank you."
        tts("I am still functioning as intended, thank you.")
    elif said in ('goodbye' or 'see ya' or 'later'):
        print "goodbye"
        tts("goodbye")
        sys.exit()


def tts(msg):
    if 'linux' in sys.platform:
        tts_prefix = 'espeak -ven+f5 -k5 -s180 '
        os.system(tts_prefix + '"' + msg + '"')
    else:
        raise OSError

def main(config):
    if 'DEBUG' not in config['state']:
        error_supress()
    try:
        tts("Hello, I am "+config['namephonetic'])

        while(True):
            mic = sr.Recognizer()
            with sr.Microphone() as source:
                mic.adjust_for_ambient_noise(source)
                print "calibrated...."
                print "Say Something!"
                audio = mic.listen(source)
            print "got audio"

            said = ""
            try:
                print "Sending audio...."
                said = mic.recognize_google(audio)
                print(config['name'] + " thinks you said '" + said + "'")
            except sr.UnknownValueError:
                print(config['name'] + " could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            say_response(said)


    except OSError:
        print "[ERROR]: Wrong OS"
        sys.exit()
################################################################################
if __name__ == '__main__':
    try:
        with open('assets/config.json') as json_config:
            config = json.load(json_config)

            main(config)
    except ValueError:
        print "[ERROR]: Wrong configuration for JSON"
        sys.exit()
