import hashlib
import os


def hash_md5(password):
    """Уязвимость: MD5 легко подбирается (быстрый, устаревший хеш)."""
    return hashlib.md5(password.encode()).hexdigest()


def hash_sha1(password):
    """Уязвимость: SHA-1 уязвим для коллизий, не подходит для паролей."""
    return hashlib.sha1(password.encode()).hexdigest()


def hash_sha512(password):
    """Уязвимость: SHA-1 уязвим для коллизий, не подходит для паролей."""
    return hashlib.sha512(password.encode()).hexdigest()


def demonstrate_hashlib() -> None:
    print("=== ДЕМО: hashlib (MD5, SHA-1, SHA-512) ===")

    while True:
        password = input('\nВведите пароль или нажмите ENTER для выхода: ')
        if not password:
            break
        os.makedirs("pwds", exist_ok=True)
        with open(os.path.join('pwds', 'custom.txt'), 'a', encoding='utf8') as f:
            f.write(f'{password}\n')

        print(f"Пароль:\t {password}")
        print(f"MD5:\t {hash_md5(password)}")
        print(f"SHA-1:\t {hash_sha1(password)}")
        print(f"SHA-512: {hash_sha512(password)}")


if __name__ == "__main__":
    demonstrate_hashlib()
