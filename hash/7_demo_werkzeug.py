from werkzeug.security import generate_password_hash, check_password_hash
import os


def demonstrate_werkzeug_password_hash():
    print("\n=== РЕШЕНИЕ С WERKZEUG (хеширование паролей) ===")
    while True:
        password = input(
            "\nВведите пароль для хеширования (ENTER - перейти к проверке): "
        )
        if not password:
            break
        os.makedirs("pwds", exist_ok=True)
        with open(os.path.join('pwds', 'custom.txt'), 'a', encoding='utf8') as f:
            f.write(f'{password}\n')
            
        hashed = generate_password_hash(password)
        print(f"✓ Пароль: {password}")
        print(f"✓ Хеш (Werkzeug): {hashed}")
        print("  Сохраните этот хеш для проверки позже.")

    print("\n=== Проверка пароля по хешу ===")
    while True:
        password_check = input("\nВведите проверяемый пароль (ENTER - выход): ")
        if not password_check:
            break

        hash_check = input("Вставьте хеш для сравнения: ")
        is_valid = check_password_hash(hash_check, password_check)
        if is_valid:
            print("✓ ПАРОЛЬ СОВПАДАЕТ С ХЕШЕМ!")
        else:
            print("✗ Пароль НЕ соответствует хешу")


if __name__ == "__main__":
    demonstrate_werkzeug_password_hash()
