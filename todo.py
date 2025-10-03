import os
import subprocess
import pickle
import sqlite3

tasks = []

def add_task(task):
    tasks.append(task)

def get_tasks():
    return tasks

# 1. eval -> bisa dieksploitasi
def insecure_eval(user_input):
    return eval(user_input)

# 2. subprocess dengan shell=True -> command injection
def run_command(cmd):
    subprocess.run(cmd, shell=True)

# 3. pickle.loads -> deserialization berbahaya
def insecure_deserialize(data_bytes):
    return pickle.loads(data_bytes)

# 4. SQL injection dengan f-string
def add_task_db(username, task):
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()
    query = f"INSERT INTO tasks (user, task) VALUES ('{username}', '{task}')"
    cur.execute(query)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_task("Belajar Python")
    add_task("Mengerjakan Tugas")
    print("Daftar tugas:")
    for i, t in enumerate(get_tasks(), 1):
        print(i, t)

    # Cek apakah dijalankan di GitHub Actions
    if os.getenv("GITHUB_ACTIONS") != "true":
        expr = input("Masukkan ekspresi Python (contoh eval): ")
        print("Eval =>", insecure_eval(expr))
