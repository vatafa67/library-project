"""Модуль для работы с читателями."""
from database import get_connection

def get_all_readers():
    """Возвращает список всех читателей."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM readers ORDER BY last_name")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_reader(last_name, first_name, student_card, group_name=None, phone=None):
    """
    Добавляет нового читателя с валидацией (Задание 4).
    """
    # Проверка на пустые значения
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
            (last_name.strip(), first_name.strip(), student_card.strip(), group_name, phone)
        )
        conn.commit()
        new_id = cursor.lastrowid
        print(f"Читатель '{last_name} {first_name}' добавлен (ID={new_id})")
        return new_id
    except Exception as e:
        print(f"Ошибка при добавлении: {e}")
        return None
    finally:
        conn.close()
