import os
import json
import subprocess
import datetime

CHECKSUM_FILE = "checksums.json"
CPVERIFY_PATH = "cpverify.exe"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def strip_quotes(s):
    """Удаляет начальные и конечные одинарные или двойные кавычки."""
    s = s.strip()
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    return s

def load_checksums():
    if os.path.exists(CHECKSUM_FILE):
        with open(CHECKSUM_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_checksums(data):
    with open(CHECKSUM_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def run_cpverify(filepath):
    """
    Выполняет cpverify.exe и возвращает хеш (без лишних пробелов).
    """
    try:
        result = subprocess.run(
            [CPVERIFY_PATH, "-mk", "-alg", "GR3411_2012_256", str(filepath)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"\n[DEBUG] cpverify завершился с ошибкой (код {e.returncode})")
        print(f"[DEBUG] stderr: {e.stderr.strip()}")
        return None
    except FileNotFoundError:
        print(f"Ошибка: не найден '{CPVERIFY_PATH}'. Убедитесь, что он доступен.")
        return None

def normalize_path(p):
    return os.path.normcase(os.path.abspath(p))

def check_dialog():
    raw_input = input("Введите путь к файлу для проверки: ").strip()
    file_path = strip_quotes(raw_input)
    if not os.path.exists(file_path):
        return f"Файл не найден: \"{file_path}\""

    norm_path = normalize_path(file_path)
    checksums = load_checksums()

    if norm_path not in checksums:
        return "Контрольная сумма для этого файла не найдена в базе."

    print("Вычисление контрольной суммы...")
    current_hash = run_cpverify(file_path)
    if not current_hash:
        return "Ошибка при вычислении хеша."

    saved_hash = checksums[norm_path]["hash"]
    if current_hash == saved_hash:
        return "УСПЕХ: Контрольные суммы совпадают."
    else:
        return f"ОШИБКА: Контрольные суммы НЕ совпадают!\nСохранённая: {saved_hash}\nТекущая:     {current_hash}"

def read_dialog():
    raw_input = input("Введите полный путь к файлу: ").strip()
    file_path = strip_quotes(raw_input)
    if not os.path.exists(file_path):
        return f"Файл не найден: \"{file_path}\""

    norm_path = normalize_path(file_path)
    checksums = load_checksums()

    if norm_path in checksums:
        return "Контрольная сумма для этого файла уже сохранена."

    print("Вычисление контрольной суммы...")
    hash_val = run_cpverify(file_path)
    if not hash_val:
        return "Ошибка при вычислении хеша."

    checksums[norm_path] = {
        "hash": hash_val,
        "added_at": datetime.datetime.now().isoformat(),
    }
    save_checksums(checksums)
    return "Контрольная сумма сохранена."

def show_dialog():
    checksums = load_checksums()
    if not checksums:
        return "Файл с контрольными суммами отсутствует или пуст."

    lines = ["Сохранённые контрольные суммы:", "-" * 50]
    for path, info in checksums.items():
        lines.append(f"{info['hash']} *\"{path}\"")
        lines.append(f"  Добавлено: {info['added_at']}")
        lines.append("")
    return "\n".join(lines)

def main():
    while True:
        clear_screen()
        print("=" * 30)
        print("Меню проверки контрольных сумм")
        print("=" * 30)
        print("1. Вычислить и сохранить контрольную сумму файла")
        print("2. Показать сохранённые контрольные суммы")
        print("3. Проверить контрольную сумму файла")
        print("4. Выход")
        choice = input("\nВыберите действие (1-4): ").strip()

        match choice:
            case "1":
                print(read_dialog())
            case "2":
                print(show_dialog())
            case "3":
                print(check_dialog())
            case "4":
                print("Выход.")
                break
            case _:
                print("Неверный выбор.")
        input("\nНажмите Enter, чтобы продолжить...")

if __name__ == "__main__":
    main()