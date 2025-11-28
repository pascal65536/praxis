import base64
from nacl.secret import SecretBox
from nacl.utils import random
import os


def demonstrate_pynacl_secretbox():


    print("\n=== РЕШЕНИЕ С PYNACL (libsodium) ===")

    key = random(SecretBox.KEY_SIZE)
    box = SecretBox(key)

    while True:
        message = input("\nВведите сообщение или нажмите ENTER для перехода ко второй части: ")
        if not message:
            break
        os.makedirs("pwds", exist_ok=True)        
        with open(os.path.join('pwds', 'custom.txt'), 'a', encoding='utf8') as f:
            f.write(f'{message}\n')

        encrypted = box.encrypt(message.encode("utf-8"))
        decrypted = box.decrypt(encrypted)
        encrypted_b64 = base64.b64encode(encrypted).decode("utf-8")

        print(f"Исходное сообщение: {message}")
        print(f"Зашифровано (Base64): {encrypted_b64}")
        print(f"Расшифровано: {decrypted.decode('utf-8')}")

    print("\n=== Проверка расшифровки по Base64: ===")
    while True:
        encrypted_input = input("\nСкопируйте зашифрованное сообщение (Base64) или ENTER для выхода: ")
        if not encrypted_input:
            break
        try:
            encrypted_bytes = base64.b64decode(encrypted_input)
            decrypted_bytes = box.decrypt(encrypted_bytes)
            print("Расшифрованное сообщение:", decrypted_bytes.decode("utf-8"))
        except Exception as e:
            print("Ошибка расшифровки:", e)



if __name__ == "__main__":
    demonstrate_pynacl_secretbox()
