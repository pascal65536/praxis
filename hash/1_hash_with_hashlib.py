import hashlib
import os


def hash_md5(password: str) -> str:
    """Уязвимость: MD5 легко подбирается (быстрый, устаревший хеш)."""
    return hashlib.md5(password.encode()).hexdigest()


def hash_sha1(password: str) -> str:
    """Уязвимость: SHA-1 уязвим для коллизий, не подходит для паролей."""
    return hashlib.sha1(password.encode()).hexdigest()


def demonstrate_hashlib() -> None:
    print("=== ДЕМО: hashlib (MD5, SHA-1) ===")

    while True:
        password = input('\nВведите пароль или нажмите ENTER для выхода: ')
        if not password:
            break
        with open(os.path.join('pwds', 'custom.txt'), 'a', encoding='utf8') as f:
            f.write(f'{password}\n')
        md5_hash = hash_md5(password)
        sha1_hash = hash_sha1(password)

        print(f"Пароль:\t{password}")
        print(f"MD5:\t{md5_hash}")
        print(f"SHA-1:\t{sha1_hash}")


if __name__ == "__main__":
    demonstrate_hashlib()
