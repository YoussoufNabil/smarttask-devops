import os
import time
from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_HOST = os.getenv('DB_HOST', 'database')
DB_NAME = os.getenv('POSTGRES_DB', 'smarttask')
DB_USER = os.getenv('POSTGRES_USER', 'smarttask')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'smarttaskpass')
DB_PORT = int(os.getenv('DB_PORT', '5432'))

def get_conn():
    return psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)

def init_db():
    for _ in range(20):
        try:
            conn = get_conn()
            with conn.cursor() as cur:
                cur.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(120) NOT NULL,
                    completed BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )''')
            conn.commit(); conn.close(); return
        except Exception:
            time.sleep(2)
    raise RuntimeError('Impossible de se connecter à PostgreSQL')

@app.get('/health')
def health():
    return jsonify({'status': 'ok'})

@app.get('/tasks')
def list_tasks():
    conn = get_conn()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute('SELECT id, title, completed, created_at FROM tasks ORDER BY id DESC')
        rows = cur.fetchall()
    conn.close()
    for row in rows:
        row['created_at'] = row['created_at'].isoformat()
    return jsonify(rows)

@app.post('/tasks')
def create_task():
    data = request.get_json(silent=True) or {}
    title = str(data.get('title', '')).strip()
    if not title:
        return jsonify({'error': 'title est obligatoire'}), 400
    conn = get_conn()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute('INSERT INTO tasks (title) VALUES (%s) RETURNING id, title, completed, created_at', (title,))
        row = cur.fetchone()
    conn.commit(); conn.close()
    row['created_at'] = row['created_at'].isoformat()
    return jsonify(row), 201

@app.patch('/tasks/<int:task_id>/toggle')
def toggle_task(task_id):
    conn = get_conn()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute('UPDATE tasks SET completed = NOT completed WHERE id=%s RETURNING id, title, completed, created_at', (task_id,))
        row = cur.fetchone()
    if not row:
        conn.close(); return jsonify({'error': 'tâche introuvable'}), 404
    conn.commit(); conn.close()
    row['created_at'] = row['created_at'].isoformat()
    return jsonify(row)

@app.delete('/tasks/<int:task_id>')
def delete_task(task_id):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute('DELETE FROM tasks WHERE id=%s RETURNING id', (task_id,))
        deleted = cur.fetchone()
    conn.commit(); conn.close()
    if not deleted: return jsonify({'error': 'tâche introuvable'}), 404
    return jsonify({'deleted': task_id})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
