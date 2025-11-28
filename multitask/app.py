from flask import Flask, request, jsonify, render_template
import hashlib
import json
import random
import time
from datetime import datetime, timedelta
import os
import behoof

app = Flask(__name__)

DATA_FILE = "client_data.json"




def generate_task_hash(numbers):
    """
    Генерирует хеш задачи на основе списка чисел
    """
    numbers_str = "".join(map(str, sorted(numbers)))
    return hashlib.sha256(numbers_str.encode()).hexdigest()


@app.route("/")
def index():
    """
    Главная страница с мониторингом воркеров
    """
    data = behoof.load_json('data', DATA_FILE, default=[])
    workers_info = analyze_workers_data(data)
    return render_template("index.html", workers_info=workers_info,         
                           now=datetime.now())


@app.route("/worker/<client_id>")
def worker_details(client_id):
    """
    Детальная информация по конкретному воркеру
    """
    data = behoof.load_json('data', DATA_FILE, default=[])
    worker_entries = [entry for entry in data if entry["client_id"] == client_id]
    
    if not worker_entries:
        return "Worker not found", 404
    
    completed_tasks = len([entry for entry in worker_entries if entry["completed"]])
    pending_tasks = len([entry for entry in worker_entries if not entry["completed"]])
    
    last_activity = max(
        [datetime.fromisoformat(entry["timestamp"].replace('Z', '+00:00')) 
         for entry in worker_entries]
    ) if worker_entries else None
    
    return render_template(
        "worker_details.html",
        client_id=client_id,
        entries=worker_entries,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        total_tasks=len(worker_entries),
        last_activity=last_activity,
        now=datetime.now()
    )


def analyze_workers_data(data):
    """
    Анализирует данные и возвращает информацию о воркерах
    """
    workers = {}
    
    for entry in data:
        client_id = entry["client_id"]
        
        if client_id not in workers:
            workers[client_id] = {
                'total_tasks': 0,
                'completed_tasks': 0,
                'pending_tasks': 0,
                'last_activity': None,
                'current_task': None,
                'first_seen': None
            }
        
        worker = workers[client_id]
        worker['total_tasks'] += 1
        
        if entry["completed"]:
            worker['completed_tasks'] += 1
        else:
            worker['pending_tasks'] += 1
            worker['current_task'] = {
                'numbers': entry["numbers"],
                'task_hash': entry["task_hash"][:16] + "...",
                'assigned_time': entry["timestamp"]
            }
        
        entry_time = datetime.fromisoformat(entry["timestamp"].replace('Z', '+00:00'))
        if worker['last_activity'] is None or entry_time > worker['last_activity']:
            worker['last_activity'] = entry_time
        
        if worker['first_seen'] is None:
            worker['first_seen'] = entry_time
    
    now = datetime.now()
    for worker_id, worker_info in workers.items():
        if worker_info['last_activity']:
            time_diff = now - worker_info['last_activity']
            worker_info['is_active'] = time_diff < timedelta(minutes=1)
        else:
            worker_info['is_active'] = False
    
    return workers


@app.route("/api/get_task", methods=["POST"])
def get_task():
    """
    Генерирует задачу для клиента
    """
    client_data = request.get_json()
    if not client_data or "client_id" not in client_data:
        msg = {"error": "client_id required"}
        return jsonify(msg), 400

    client_id = client_data["client_id"]
    numbers = [random.randint(1, 100) for _ in range(10)]
    task_hash = generate_task_hash(numbers)
    data = behoof.load_json('data', DATA_FILE, default=[])
    timestamp = datetime.now().isoformat()
    new_entry = {
        "timestamp": timestamp,
        "client_id": client_id,
        "numbers": numbers,
        "task_hash": task_hash,
        "sorted_numbers": None,
        "completed": False,
    }

    data.append(new_entry)
    behoof.save_json('data', DATA_FILE, data)
    return jsonify({"numbers": numbers, "task_hash": task_hash})


@app.route("/api/submit_solution", methods=["POST"])
def submit_solution():
    """
    Принимает решение от клиента
    """
    sd = request.get_json()
    if not sd or "sorted_numbers" not in sd or "task_hash" not in sd:
        msg = {"error": "sorted_numbers and task_hash required"}
        return jsonify(msg), 400

    sorted_numbers = sd["sorted_numbers"]
    task_hash = sd["task_hash"]
    client_id = sd.get("client_id")
    data = behoof.load_json('data', DATA_FILE, default=[])
    task_found = False
    for entry in data:
        if entry["task_hash"] == task_hash and not entry["completed"]:
            expected_sorted = sorted(entry["numbers"])
            if sorted_numbers != expected_sorted:
                msg = {"status": "error", "message": "Incorrect sorting"}
                return jsonify(msg), 400
            entry["sorted_numbers"] = sorted_numbers
            entry["completed"] = True
            entry["completion_time"] = datetime.now().isoformat()
            task_found = True
            behoof.save_json('data', DATA_FILE, data)
            return jsonify(
                {
                    "status": "success",
                    "message": "Solution accepted",
                    "client_id": entry["client_id"],
                    "timestamp": entry["timestamp"],
                    "original_numbers": entry["numbers"],
                    "sorted_numbers": sorted_numbers,
                }
            )

    if not task_found:
        msg = {"status": "error", "message": "Task not found or already completed"}
        return (jsonify(msg), 404)


@app.route("/api/client_data/<client_id>", methods=["GET"])
def get_client_data(client_id):
    """
    Возвращает данные по конкретному клиенту
    """
    data = behoof.load_json('data', DATA_FILE, default=[])
    client_entries = [entry for entry in data if entry["client_id"] == client_id]

    return jsonify(
        {
            "client_id": client_id,
            "entries": client_entries,
            "total_tasks": len(client_entries),
            "completed_tasks": len(
                [entry for entry in client_entries if entry["completed"]]
            ),
        }
    )


@app.route("/api/all_data", methods=["GET"])
def get_all_data():
    """
    Возвращает все данные
    """
    return jsonify(behoof.load_json('data', DATA_FILE, default=[]))


if __name__ == "__main__":   
    behoof.load_json('data', DATA_FILE, default=[])
    app.run(debug=True, port=5000)