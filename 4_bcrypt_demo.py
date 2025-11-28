import bcrypt
import os

def demonstrate_bcrypt():
    """Демо bcrypt: хеширование и проверка паролей."""
    print("=== ДЕМО: BCRYPT (безопасное хеширование паролей) ===")
    
    # Словарь для хранения паролей и их хешей
    password_hashes = {}
    
    # === ЧАСТЬ 1: Генерация хешей ===
    print("\n--- Генерация хешей bcrypt ---")
    while True:
        password = input("\nВведите пароль (ENTER - перейти к проверке): ")
        if not password:
            break
            
        # Сохранение в файл
        os.makedirs("pwds", exist_ok=True)
        with open(os.path.join("pwds", "custom.txt"), "a", encoding="utf8") as f:
            f.write(f"{password}\n")
        
        # Создание хеша
        hashed = hash_bcrypt(password)
        password_hashes[password] = hashed
        
        print(f"✓ Пароль:      {password}")
        print(f"✓ Хеш bcrypt:  {hashed.decode()}")
        print("  Скопируйте хеш для проверки ниже!")
        print()
    
    # === ЧАСТЬ 2: Проверка хешей ===
    print("\n=== ПРОВЕРКА ПАРОЛЕЙ ПО ХЕШАМ ===")
    while True:
        print("\n(Введите пароль и хеш для проверки)")
        test_password = input("Введите проверяемый пароль (ENTER - выход): ")
        if not test_password:
            break
            
        hash_input = input("Вставьте bcrypt хеш: ").strip()
        
        try:
            # Проверка пароля
            is_valid = verify_bcrypt(test_password, hash_input.encode())
            
            if is_valid:
                print("✓ ПАРОЛЬ СОВПАДАЕТ С ХЕШЕМ!")
            else:
                print("✗ Пароль НЕ соответствует хешу")
                
        except Exception as e:
            print(f"✗ Ошибка проверки: {e}")
            print("  Проверьте правильность хеша!")


def hash_bcrypt(password: str) -> bytes:
    """Безопасное хеширование паролей с bcrypt (автосоль)."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_bcrypt(password: str, hashed: bytes) -> bool:
    """Проверка пароля по bcrypt хешу."""
    return bcrypt.checkpw(password.encode(), hashed)


if __name__ == "__main__":
    demonstrate_bcrypt()
