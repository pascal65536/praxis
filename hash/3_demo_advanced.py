import os


def advanced_custom_hash(password):
    """
    УЯЗВИМОСТЬ: "сложная" самодельная хеш-функция.
    Выглядит круто, но имеет серьезные проблемы:
    1. Предсказуемый seed (42)
    2. Маленькое конечное пространство (32 бита)
    3. Слабый XOR с ключами
    4. Легко обратимые операции
    5. Много коллизий при переборе
    """
    if not password:
        return "00"

    # Инициализация с секретным seed, который на самом деле не секретный
    state = 42
    hash_value = 0
    length = len(password)

    # 1 фаза: полиномиальное хеширование с ротацией
    for i, char in enumerate(password):
        # Ротация state влево на 3 бита
        state = ((state << 3) | (state >> 29)) & 0xFFFFFFFF
        # Полином с разными коэффициентами
        coeff = (i * 37 + length * 41 + 43) % 256
        state = (state * 31 + ord(char) * coeff) % (1 << 32)

    # 2 фаза: XOR с "секретными" ключами
    secret_keys = [0xDEADBEEF, 0xCAFEBABE, 0x1337C0DE, 0xBADC0FFEE]
    for key in secret_keys:
        hash_value ^= (state + key) & 0xFFFFFFFF
        hash_value = ((hash_value << 7) | (hash_value >> 25)) & 0xFFFFFFFF

    # 3 фаза: финальное смешивание
    hash_value = (hash_value * 0x85EBCA6B) ^ (hash_value >> 16)
    hash_value = ((hash_value << 11) | (hash_value >> 21)) & 0xFFFFFFFF

    # Возвращаем первые 8 hex символов (32 бита)
    return format(hash_value & 0xFFFFFFFF, "08x")


def demonstrate_advanced_custom_hash() -> None:
    print("=== ДЕМО: advanced_custom_hash (сложная самодельная) ===")

    while True:
        password = input("\nВведите пароль или нажмите ENTER для выхода: ")
        if not password:
            break
        os.makedirs("pwds", exist_ok=True)
        with open(os.path.join("pwds", "custom.txt"), "a", encoding="utf8") as f:
            f.write(f"{password}\n")
        print(f"Пароль:\t{password}")
        print(f"Custom Hash:\t{advanced_custom_hash(password)}")


if __name__ == "__main__":
    demonstrate_advanced_custom_hash()
