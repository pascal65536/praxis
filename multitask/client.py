import requests
import sys
import time
import random


class SortClient:
    def __init__(self, client_id, server_url="http://localhost:5000"):
        self.client_id = client_id
        self.server_url = server_url

    def get_task(self):
        """Получает задачу от сервера"""
        try:
            json = {"client_id": self.client_id}
            url = f"{self.server_url}/api/get_task"
            response = requests.post(url, json=json, timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"[{self.client_id}] Получена задача: {data['numbers']}")
                return data
            else:
                print(f"[{self.client_id}] Ошибка получения задачи: {response.text}")
                return None
        except Exception as e:
            print(f"[{self.client_id}] Ошибка соединения: {e}")
            return None

    def solve_task(self, numbers):
        """Решает задачу - сортирует числа (с небольшой задержкой)"""
        time.sleep(random.uniform(1, 30))
        return sorted(numbers)

    def submit_solution(self, sorted_numbers, task_hash):
        """Отправляет решение на сервер"""
        try:
            response = requests.post(
                f"{self.server_url}/api/submit_solution",
                json={
                    "client_id": self.client_id,
                    "sorted_numbers": sorted_numbers,
                    "task_hash": task_hash,
                },
                timeout=5,
            )

            return response.json()
        except Exception as e:
            print(f"[{self.client_id}] Ошибка отправки решения: {e}")
            return {"status": "error", "message": str(e)}

    def run_once(self):
        """Выполняет одну задачу"""
        task = self.get_task()
        if not task:
            return False
        sorted_numbers = self.solve_task(task["numbers"])
        print(f"[{self.client_id}] Отсортированные числа: {sorted_numbers}")
        result = self.submit_solution(sorted_numbers, task["task_hash"])
        print(f"[{self.client_id}] Результат: {result.get('status', 'unknown')}")
        return True


if __name__ == "__main__":
    worker_name = sys.argv[1]
    worker = SortClient(worker_name)
    print(f"🚀 Starting workers {worker.client_id}")
    print("🌐 Web interface available at: http://localhost:5000")
    while True:
        worker.run_once()
        time.sleep(3)
