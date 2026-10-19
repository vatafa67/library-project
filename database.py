"""Модуль для работы с БД. Добавлена таблица users."""
import sqlite3
import hashlib

DB_PATH = 'library.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, author TEXT NOT NULL, year INTEGER, quantity INTEGER DEFAULT 1)")
    cursor.execute("CREATE TABLE IF NOT EXISTS readers (id INTEGER PRIMARY KEY AUTOINCREMENT, last_name TEXT NOT NULL, first_name TEXT NOT NULL, student_card TEXT UNIQUE NOT NULL, group_name TEXT, phone TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS issues (id INTEGER PRIMARY KEY AUTOINCREMENT, book_id INTEGER NOT NULL, reader_id INTEGER NOT NULL, issue_date DATE NOT NULL, due_date DATE NOT NULL, return_date DATE)")
    
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, role TEXT NOT NULL, reader_id INTEGER)")
    
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        admin_pass = hash_password("admin123")
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", ("admin", admin_pass, "admin"))
    conn.commit()
    conn.close()
    print("База данных инициализирована")
