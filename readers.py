"""
Модуль для работы с читателями.
Содержит CRUD-операции для таблицы readers.
"""
import sqlite3
from database import get_connection


def get_all_readers():
    """Возвращает список всех читателей."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM readers ORDER BY last_name")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_reader_by_id(reader_id):
    """Возвращает читателя по ID или None."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM readers WHERE id = ?", (reader_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def add_reader(last_name, first_name, student_card, group_name=None, phone=None):
    """
    Добавляет нового читателя.

    Валидирует обязательные поля (ФИО и номер студенческого билета)
    и возвращает ID созданной записи. При ошибке возвращает None.
    """
    # Валидация обязательных полей
    if not last_name or not last_name.strip():
        raise ValueError("Фамилия не может быть пустой")
    if not first_name or not first_name.strip():
        raise ValueError("Имя не может быть пустым")
    if not student_card or not student_card.strip():
        raise ValueError("Номер студенческого билета обязателен")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO readers (last_name, first_name, student_card, group_name, phone) "
            "VALUES (?, ?, ?, ?, ?)",
            (last_name.strip(), first_name.strip(), student_card.strip(),
             group_name, phone)
        )
        conn.commit()
        new_id = cursor.lastrowid
        print(f"Читатель '{last_name} {first_name}' добавлен (ID={new_id})")
        return new_id
    except sqlite3.IntegrityError:
        print(f"Читатель с билетом {student_card} уже существует")
        return None
    finally:
        conn.close()


def update_reader(reader_id, **fields):
    """Обновляет поля читателя."""
    if not fields:
        return False
    conn = get_connection()
    cursor = conn.cursor()
    updates = [f"{k} = ?" for k in fields.keys()]
    values = list(fields.values()) + [reader_id]
    try:
        cursor.execute(
            f"UPDATE readers SET {', '.join(updates)} WHERE id = ?",
            values
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def delete_reader(reader_id):
    """
    Удаляет читателя по ID с проверками.

    Не позволяет удалить читателя, у которого есть активные (невозвращённые)
    книги. Возвращает True при успешном удалении, False — если читатель
    не найден или у него есть активные выдачи.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 1. Проверяем, что читатель существует
        cursor.execute("SELECT last_name, first_name FROM readers WHERE id = ?",
                       (reader_id,))
        reader = cursor.fetchone()
        if not reader:
            print(f"Читатель с ID {reader_id} не найден.")
            return False

        # 2. Проверяем, нет ли активных выдач
        cursor.execute(
            "SELECT COUNT(*) FROM issues "
            "WHERE reader_id = ? AND return_date IS NULL",
            (reader_id,)
        )
        active_count = cursor.fetchone()[0]
        if active_count > 0:
            print(f"Нельзя удалить читателя {reader['last_name']} "
                  f"{reader['first_name']}: у него {active_count} активных выдач.")
            return False

        # 3. Удаляем
        cursor.execute("DELETE FROM readers WHERE id = ?", (reader_id,))
        conn.commit()
        print(f"Читатель {reader['last_name']} {reader['first_name']} удалён.")
        return True

    except sqlite3.IntegrityError as e:
        print(f"Ошибка целостности БД: {e}")
        return False
    finally:
        conn.close()
