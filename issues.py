"""
Модуль для работы с выдачей и возвратом книг.
"""
import sqlite3
from datetime import datetime, timedelta
from database import get_connection


def issue_book(book_id, reader_id, days=30):
    """Оформляет выдачу книги читателю."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()

    if not book or book['quantity'] <= 0:
        conn.close()
        return False, "Книга отсутствует в наличии"

    issue_date = datetime.now().date()
    due_date = issue_date + timedelta(days=days)

    try:
        cursor.execute('''
            INSERT INTO issues (book_id, reader_id, issue_date, due_date, status)
            VALUES (?, ?, ?, ?, 'выдана')
        ''', (book_id, reader_id, issue_date, due_date))

        cursor.execute(
            "UPDATE books SET quantity = quantity - 1 WHERE id = ?",
            (book_id,)
        )

        conn.commit()
        return True, f"Книга выдана. Срок возврата: {due_date}"
    except sqlite3.Error as e:
        return False, str(e)
    finally:
        conn.close()


def return_book(issue_id):
    """Оформляет возврат книги."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM issues WHERE id = ? AND return_date IS NULL",
        (issue_id,)
    )
    issue = cursor.fetchone()

    if not issue:
        conn.close()
        return False, "Выдача не найдена или уже закрыта"

    today = datetime.now().date()
    try:
        cursor.execute(
            "UPDATE issues SET return_date = ?, status = 'возвращена' WHERE id = ?",
            (today, issue_id)
        )
        cursor.execute(
            "UPDATE books SET quantity = quantity + 1 WHERE id = ?",
            (issue['book_id'],)
        )
        conn.commit()
        return True, "Книга возвращена"
    except sqlite3.Error as e:
        return False, str(e)
    finally:
        conn.close()


def get_all_issues():
    """Возвращает все выдачи с информацией о книгах и читателях."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            issues.id,
            books.title AS book_title,
            readers.last_name || ' ' || readers.first_name AS reader_name,
            issues.issue_date,
            issues.due_date,
            issues.return_date,
            issues.status
        FROM issues
        JOIN books ON issues.book_id = books.id
        JOIN readers ON issues.reader_id = readers.id
        ORDER BY issues.issue_date DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_active_issues():
    """Возвращает только активные выдачи (книги не возвращены)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            issues.id,
            books.title AS book_title,
            readers.last_name || ' ' || readers.first_name AS reader_name,
            issues.issue_date,
            issues.due_date
        FROM issues
        JOIN books ON issues.book_id = books.id
        JOIN readers ON issues.reader_id = readers.id
        WHERE issues.return_date IS NULL
        ORDER BY issues.due_date
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
