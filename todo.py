# todo.py
# Versi yang menyertakan contoh aliran data "tainted -> sink"
# aman di CI karena blok if False tidak dieksekusi, namun CodeQL melihatnya statis.

import os
import subprocess
import pickle
import sqlite3

tasks = []

def add_task(task):
    tasks.append(task)

def get_tasks():
    return tasks

# 1) eval -> remote code execution risk
def insecure_eval(user_input):
    return eval(user_input)

# 2) subprocess.run with shell=True -> command injection risk
def run_command(cmd):
    subprocess.run(cmd, shell=True)

# 3) pickle.loads -> insecure deserialization
def insecure_deserialize(data_bytes):
    return pickle.loads(data_bytes)

# 4) SQL via f-string -> SQL injection
def add_task_db(username, task):
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()
    query = f"INSERT INTO tasks (user, task) VALUES ('{username}', '{task}')"
    cur.execute(query)
    conn.commit()
    conn.close()

# ======= contoh "tainted flow" untuk CodeQL (tidak akan dijalankan) =======
# Blok ini tidak dieksekusi (if False), jadi CI tidak akan hang.
# Namun CodeQL melihat bahwa input() (sumber tak dipercaya) dipakai kemudian di sink berbahaya,
# sehingga biasanya akan membuat alert.
if False:
    # 1) input -> eval
    tainted_expr = input("masukkan ekspresi (demo): ")
    insecure_eval(tainted_expr)

    # 2) input -> subprocess.run(..., shell=True)
    tainted_cmd = input("masukkan perintah shell (demo): ")
    run_command(tainted_cmd)

    # 3) input -> pickle.loads (simulasi bytes)
    tainted_bytes = input("masukkan serialized (demo): ").encode('utf-8')
    insecure_deserialize(tainted_bytes)

    # 4) input -> SQL via f-string
    tainted_user = input("masukkan username (demo): ")
    add_task_db(tainted_user, "contoh tugas")

# ===== runtime normal (non-interaktif di CI) =====
def interactive_mode():
    # jika dijalankan di GitHub Actions, env ini = "true"
    return os.getenv("GITHUB_ACTIONS") != "true"

if __name__ == "__main__":
    add_task("Belajar Python")
    add_task("Mengerjakan Tugas")
    print("Daftar tugas (non-interaktif):")
    for i, t in enumerate(get_tasks(), 1):
        print(i, t)

    if interactive_mode():
        # ini hanya jalan di lokal (pengguna)
        expr = input("Masukkan ekspresi Python (contoh eval): ")
        print("Eval =>", insecure_eval(expr))
    else:
        print("CI detected — skipping interactive input.")
