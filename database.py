"""
Модуль для работы с базой данных "Студенческая библиотека".
Отвечает за подключение и инициализацию таблиц.
"""
import sqlite3

DB_PATH = 'library.db'


def get_connection():
    """Возвращает соединение с базой данных."""
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Создаёт все таблицы, если их нет."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            quantity INTEGER DEFAULT 1
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            student_card TEXT UNIQUE NOT NULL,
            group_name TEXT,
            phone TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            reader_id INTEGER NOT NULL,
            issue_date DATE NOT NULL,
            due_date DATE NOT NULL,
            return_date DATE,
            status TEXT DEFAULT 'выдана',
            FOREIGN KEY (book_id) REFERENCES books (id),
            FOREIGN KEY (reader_id) REFERENCES readers (id)
        )
    ''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_database()
    print("База данных инициализирована")
