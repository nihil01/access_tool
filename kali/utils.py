import random
import os


def random_name() -> str:
    abc = "qwertyuiopasdfghjklzxcvbnm1234567890"
    return "".join([abc[random.randint(0, len(abc) - 1)] for _ in range(0, len(abc) - 20)])


def write_to_disk(path: str, chunk: bytes)-> None:
        with open(path, 'wb') as file:
            file.write(chunk)
