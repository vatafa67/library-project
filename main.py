"""
Главный модуль приложения "Студенческая библиотека".
Содержит меню и точку входа.
"""
from database import init_database
from books import (
    get_all_books, search_books_by_author, add_book,
    update_book, delete_book, count_books
)
from readers import (
    get_all_readers, add_reader, update_reader, delete_reader
)
from issues import issue_book, return_book, get_all_issues, get_active_issues
from reports import get_debtors, get_most_popular_books, get_library_stats


def print_books(books):
    """Выводит список книг."""
    if not books:
        print("Книг не найдено.")
        return
    print(f"\n{'ID':<4} {'Название':<30} {'Автор':<20} {'Год':<6} {'Кол-во':<6}")
    print("-" * 70)
    for b in books:
        print(f"{b['id']:<4} {b['title'][:28]:<30} {b['author'][:18]:<20} "
              f"{b['year'] or '-':<6} {b['quantity']:<6}")


def print_readers(readers):
    """Выводит список читателей."""
    if not readers:
        print("Читателей не найдено.")
        return
    print(f"\n{'ID':<4} {'Фамилия':<15} {'Имя':<15} {'Билет':<12} {'Группа':<10}")
    print("-" * 70)
    for r in readers:
        print(f"{r['id']:<4} {r['last_name'][:13]:<15} {r['first_name'][:13]:<15} "
              f"{r['student_card']:<12} {r['group_name'] or '-':<10}")


def print_issues(issues):
    """Выводит список выдач."""
    if not issues:
        print("Выдач не найдено.")
        return
    print(f"\n{'ID':<4} {'Книга':<25} {'Читатель':<20} {'Выдана':<12} {'Срок':<12}")
    print("-" * 80)
    for i in issues:
        print(f"{i['id']:<4} {i['book_title'][:23]:<25} {i['reader_name'][:18]:<20} "
              f"{str(i['issue_date']):<12} {str(i['due_date']):<12}")


def main():
    """Главная функция с меню."""
    init_database()

    while True:
        print("\n" + "=" * 50)
        print(" СИСТЕМА УПРАВЛЕНИЯ БИБЛИОТЕКОЙ")
        print("=" * 50)
        print("1. Показать все книги")
        print("2. Поиск книг по автору")
        print("3. Добавить книгу")
        print("4. Удалить книгу")
        print("5. Показать всех читателей")
        print("6. Добавить читателя")
        print("7. Оформить выдачу")
        print("8. Оформить возврат")
        print("9. Показать все выдачи")
        print("10. Список должников")
        print("11. Популярные книги")
        print("12. Статистика")
        print("0. Выход")
        print("=" * 50)

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            print_books(get_all_books())
        elif choice == "2":
            author = input("Автор: ")
            print_books(search_books_by_author(author))
        elif choice == "3":
            title = input("Название: ")
            author = input("Автор: ")
            year = input("Год (Enter — пропустить): ")
            year = int(year) if year.isdigit() else None
            qty = input("Количество (Enter = 1): ")
            qty = int(qty) if qty.isdigit() else 1
            add_book(title, author, year, qty)
            print("Книга добавлена")
        elif choice == "4":
            print_books(get_all_books())
            book_id = int(input("ID книги для удаления: "))
            if delete_book(book_id):
                print("Книга удалена")
            else:
                print("Книга не найдена")
        elif choice == "5":
            print_readers(get_all_readers())
        elif choice == "6":
            last_name = input("Фамилия: ")
            first_name = input("Имя: ")
            card = input("Номер билета: ")
            group = input("Группа: ")
            phone = input("Телефон: ")
            if add_reader(last_name, first_name, card, group, phone):
                print("Читатель добавлен")
        elif choice == "7":
            print_books(get_all_books())
            book_id = int(input("ID книги: "))
            print_readers(get_all_readers())
            reader_id = int(input("ID читателя: "))
            ok, msg = issue_book(book_id, reader_id)
            print(("[OK] " if ok else "[Ошибка] ") + msg)
        elif choice == "8":
            print_issues(get_active_issues())
            issue_id = int(input("ID выдачи для возврата: "))
            ok, msg = return_book(issue_id)
            print(("[OK] " if ok else "[Ошибка] ") + msg)
        elif choice == "9":
            print_issues(get_all_issues())
        elif choice == "10":
            debtors = get_debtors()
            if debtors:
                for d in debtors:
                    print(f"{d['reader_name']} — {d['title']} "
                          f"(просрочка {int(d['days_overdue'])} дн.)")
            else:
                print("Нет должников")
        elif choice == "11":
            for b in get_most_popular_books():
                print(f"{b['title']} — {b['issue_count']} выдач")
        elif choice == "12":
            stats = get_library_stats()
            print(f"Книг: {stats['total_books']}")
            print(f"Читателей: {stats['total_readers']}")
            print(f"Активных выдач: {stats['active_issues']}")
            print(f"Должников: {stats['debtors']}")
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный выбор")


if __name__ == '__main__':
    main()
