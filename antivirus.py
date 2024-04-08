import os
import subprocess


def exclude_path_antivirus():
    dir_to_add = os.getcwd()
    all_commands = ["powershell.exe"]
    command = "Add-MpPreference -ExclusionPath " + dir_to_add
    all_commands.append(command)
    process = subprocess.run(all_commands, shell=True, capture_output=True, stdin=subprocess.DEVNULL)

    output = process.stderr.decode('cp866')
    if output == "":
        print("Added path to exclusion : " + dir_to_add)
        msg = process.stdout.decode('cp866')
    else:
        print("Couldn't add to exclusion : " + dir_to_add)
        msg = process.stderr.decode('cp866') + str(dir_to_add)
    return msg

