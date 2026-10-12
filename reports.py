"""
Модуль для отчётов и статистики.
"""
from datetime import datetime
from database import get_connection


def get_debtors():
    """Возвращает список должников (просроченные книги)."""
    today = datetime.now().date()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            readers.last_name || ' ' || readers.first_name AS reader_name,
            readers.group_name,
            readers.phone,
            books.title,
            issues.due_date,
            julianday(?) - julianday(issues.due_date) AS days_overdue
        FROM issues
        JOIN readers ON issues.reader_id = readers.id
        JOIN books ON issues.book_id = books.id
        WHERE issues.return_date IS NULL
          AND issues.due_date < ?
        ORDER BY days_overdue DESC
    ''', (today, today))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_most_popular_books(limit=5):
    """Возвращает топ-N популярных книг по количеству выдач."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            books.title,
            books.author,
            COUNT(issues.id) AS issue_count
        FROM books
        LEFT JOIN issues ON books.id = issues.book_id
        GROUP BY books.id
        ORDER BY issue_count DESC
        LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_library_stats():
    """Возвращает общую статистику библиотеки."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM readers")
    total_readers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM issues WHERE return_date IS NULL")
    active_issues = cursor.fetchone()[0]

    today = datetime.now().date()
    cursor.execute(
        "SELECT COUNT(DISTINCT reader_id) FROM issues "
        "WHERE return_date IS NULL AND due_date < ?",
        (today,)
    )
    debtors = cursor.fetchone()[0]

    conn.close()
    return {
        "total_books": total_books,
        "total_readers": total_readers,
        "active_issues": active_issues,
        "debtors": debtors
    }
