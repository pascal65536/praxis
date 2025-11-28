import os
import base64
import hashlib
from nacl.secret import SecretBox
from nacl.utils import random as nacl_random
from werkzeug.security import check_password_hash


def hash_md5(word):
    return hashlib.md5(word.encode()).hexdigest()


def hash_sha1(word):
    return hashlib.sha1(word.encode()).hexdigest()


def hash_sha512(word):
    return hashlib.sha512(word.encode()).hexdigest()


def check_werkzeug_hash(stored_hash, word):
    try:
        return check_password_hash(stored_hash, word)
    except ValueError:
        return False


# Инициализируем ключ и box один раз в начале
key = nacl_random(SecretBox.KEY_SIZE)  # 32 байта
box = SecretBox(key)


def check_libsodium_encrypted(stored_encrypted_b64, word):
    """Проверяет, соответствует ли шифротекст в base64 шифрованию слова с текущим ключом"""
    try:
        # Декодируем сохраненный шифротекст
        stored_encrypted_bytes = base64.b64decode(stored_encrypted_b64)
        
        # Шифруем слово заново с тем же ключом
        test_encrypted = box.encrypt(word.encode())
        
        # Сравниваем шифротексты (base64, чтобы удобней сравнивать строки)
        return base64.b64encode(test_encrypted).decode() == stored_encrypted_b64
    except Exception:
        return False


if __name__ == "__main__":
    os.makedirs("pwds", exist_ok=True)
    combine_lst = []
    for filename in os.listdir("pwds"):
        filepath = os.path.join("pwds", filename)
        if os.path.isfile(filepath):
            with open(filepath, "r", encoding="utf8") as f:
                filestr = f.read()
            combine_lst.extend(filestr.splitlines())

    hash_input = input("Введите хеш: ").strip()
    msg = None

    for word in set(combine_lst):
        if hash_input == hash_md5(word):
            msg = f"Хеш пароля найден (MD5): {word}"
            break
        elif hash_input == hash_sha1(word):
            msg = f"Хеш пароля найден (SHA1): {word}"
            break
        elif hash_input == hash_sha512(word):
            msg = f"Хеш пароля найден (SHA512): {word}"
            break
        elif check_werkzeug_hash(hash_input, word):
            msg = f"Хеш пароля найден (werkzeug): {word}"
            break
        elif check_libsodium_encrypted(hash_input, word):
            msg = f"Хеш пароля найден (libsodium): {word}"
            break

    print(msg if msg else "Ничего не найдено")
