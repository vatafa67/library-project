"""
Модуль для работы с книгами.
Содержит CRUD-операции для таблицы books.
"""
import sqlite3
from database import get_connection


def get_all_books():
    """Возвращает список всех книг."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books ORDER BY title")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_book_by_id(book_id):
    """Возвращает книгу по ID или None."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def search_books_by_author(author):
    """Ищет книги по автору."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE author LIKE ?", (f'%{author}%',))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def add_book(title, author, year=None, quantity=1):
    """Добавляет новую книгу."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO books (title, author, year, quantity) VALUES (?, ?, ?, ?)",
            (title, author, year, quantity)
        )
        conn.commit()
        book_id = cursor.lastrowid
        return book_id
    except sqlite3.Error as e:
        print(f"Ошибка: {e}")
        return None
    finally:
        conn.close()


def update_book(book_id, **fields):
    """Обновляет поля книги."""
    if not fields:
        return False
    conn = get_connection()
    cursor = conn.cursor()
    updates = [f"{k} = ?" for k in fields.keys()]
    values = list(fields.values()) + [book_id]
    try:
        cursor.execute(
            f"UPDATE books SET {', '.join(updates)} WHERE id = ?",
            values
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def delete_book(book_id):
    """Удаляет книгу по ID."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def count_books():
    """Возвращает общее количество книг."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM books")
    count = cursor.fetchone()[0]
    conn.close()
    return count
