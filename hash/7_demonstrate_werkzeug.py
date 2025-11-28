from werkzeug.security import generate_password_hash, check_password_hash

def demonstrate_werkzeug_password_hash():
    print("\n=== РЕШЕНИЕ С WERKZEUG (хеширование паролей) ===")
    
    hashes = {}
    
    # Часть 1: генерация хеша
    while True:
        password = input("\nВведите пароль для хеширования (ENTER - перейти к проверке): ")
        if not password:
            break
        
        hashed = generate_password_hash(password)
        hashes[password] = hashed
        
        print(f"Пароль: {password}")
        print(f"Хеш (Werkzeug): {hashed}")
        print("Сохраните этот хеш для проверки позже.")
    
    # Часть 2: проверка пароля по хешу
    print("\n=== Проверка пароля по хешу ===")
    while True:
        password_check = input("\nВведите проверяемый пароль (ENTER - выход): ")
        if not password_check:
            break
        
        hash_check = input("Вставьте хеш для сравнения: ")
        
        # Проверка пароля
        is_valid = check_password_hash(hash_check, password_check)
        
        if is_valid:
            print("✓ ПАРОЛЬ СОВПАДАЕТ С ХЕШЕМ!")
        else:
            print("✗ Пароль НЕ соответствует хешу")


if __name__ == "__main__":
    demonstrate_werkzeug_password_hash()
