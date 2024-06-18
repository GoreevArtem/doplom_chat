import time
import hashlib
import os


def create_unique_filename(original_filename: str) -> str:
    # Получение расширения файла
    _, ext = os.path.splitext(original_filename)
    # Создание хеша на основе имени файла и текущего времени
    hash_object = hashlib.sha256((original_filename + str(time.time())).encode())
    unique_filename = hash_object.hexdigest() + ext
    return unique_filename
