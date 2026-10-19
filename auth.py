"""Модуль авторизации."""
from database import get_connection, hash_password

def login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    pwd_hash = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, pwd_hash))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def register_reader(username, password, reader_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash, role, reader_id) VALUES (?, ?, 'user', ?)", (username, hash_password(password), reader_id))
        conn.commit()
        return True
    except Exception as e:
        return False
    finally:
        conn.close()
