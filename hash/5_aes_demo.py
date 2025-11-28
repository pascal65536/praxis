import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import secrets


def ecb_encrypt(data, key):
    """Уязвимость: режим ECB раскрывает структуру данных."""
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(encrypted).decode()


def weak_encrypt_cbc(data, key):
    """Уязвимость: фиксированный IV в CBC."""
    iv = b"0123456789ABCDEF"  # фиксированный IV — опасно
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(iv + encrypted).decode()


def weak_decrypt_cbc(encrypted_data, key):
    data = base64.b64decode(encrypted_data)
    iv = data[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(data[16:]), AES.block_size)
    return decrypted.decode()


def encrypt_aes_gcm(data, key):
    """Пример безопасного шифрования AES-GCM."""
    nonce = secrets.token_bytes(16)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    encrypted, tag = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(nonce + tag + encrypted).decode()


def decrypt_aes_gcm(encrypted_data, key):
    data = base64.b64decode(encrypted_data)
    nonce = data[:16]
    tag = data[16:32]
    encrypted = data[32:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(encrypted, tag).decode()


def demonstrate_aes() -> None:
    print("=== ДЕМО: AES и типичные ошибки ===")
    key = os.urandom(16)

    # ECB
    print("\n--- Режим ECB ---")
    data1 = "AAAAAABBBBBBAAAAAABBBBBB"
    data2 = "AAAAAABBBBBBAAAAAABBBBB"
    print(f"Исходные данные 1: {data1}")
    print(f"Исходные данные 2: {data2}")
    print(f"ECB шифртекст 1:   {ecb_encrypt(data1, key)}")
    print(f"ECB шифртекст 2:   {ecb_encrypt(data2, key)}")
    print("Вывод: повторяющиеся блоки дают повторяющиеся блоки шифртекста.")

    # CBC с фиксированным IV
    print("\n--- CBC с фиксированным IV ---")
    msg = "ОТ СОВЕТСКОГО ИНФОРМБЮРО"
    enc1 = weak_encrypt_cbc(msg, key)
    enc2 = weak_encrypt_cbc(msg, key)
    print(f"Сообщение: {msg}")
    print(f"CBC шифртекст 1: {enc1}")
    print(f"CBC шифртекст 2: {enc2}")
    print("Вывод: одинаковые сообщения -> одинаковый шифртекст, т.к. IV фиксирован.")

    # AES-GCM (безопасный пример)
    print("\n--- AES-GCM (безопасный пример) ---")
    msg2 = "Секретное сообщение (GCM)"
    enc = encrypt_aes_gcm(msg2, key)
    dec = decrypt_aes_gcm(enc, key)
    print(f"Исходное:     {msg2}")
    print(f"Зашифровано:  {enc}")
    print(f"Расшифровано: {dec}")
    print("Вывод: GCM обеспечивает и конфиденциальность, и целостность.")


if __name__ == "__main__":
    demonstrate_aes()
