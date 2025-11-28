import os


def custom_hash(password):
    """
    Уязвимость: самодельная хеш-функция.
    Очень маленькое пространство значений (0–255), легко перебирается
    Даёт много коллизий.
    """
    result = 0
    for char in password:
        result = (result * 31 + ord(char)) % 256
    return format(result, "02x")


def demonstrate_custom_hash() -> None:
    print("=== ДЕМО: custom_hash ===")

    while True:
        password = input("\nВведите пароль или нажмите ENTER для выхода: ")
        if not password:
            break
        with open(os.path.join("pwds", "custom.txt"), "a", encoding="utf8") as f:
            f.write(f"{password}\n")
        print(f"Пароль:\t{password}")
        print(f"Custom Hash:\t{custom_hash(password)}")


if __name__ == "__main__":
    demonstrate_custom_hash()
