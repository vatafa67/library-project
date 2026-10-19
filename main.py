"""Главный модуль с авторизацией."""
from database import init_database
from auth import login

def show_login_screen():
    print("=" * 40)
    print(" ВХОД В СИСТЕМУ 'БИБЛИОТЕКА'")
    print("=" * 40)
    username = input("Логин: ")
    password = input("Пароль: ")
    return login(username, password)

def menu_admin():
    print("\n--- МЕНЮ БИБЛИОТЕКАРЯ ---")
    print("1. Все книги\n2. Добавить книгу\n3. Удалить книгу\n0. Выход")

def menu_user():
    print("\n--- МЕНЮ ЧИТАТЕЛЯ ---")
    print("1. Каталог книг\n2. Поиск по автору\n0. Выход")

def main():
    init_database()
    user = show_login_screen()
    if not user:
        print(" Неверный логин или пароль!")
        return
    print(f"\n Добро пожаловать, {user['username']}! Ваша роль: {user['role']}")
    while True:
        if user['role'] == 'admin':
            menu_admin()
            choice = input("Выберите действие: ")
            if choice == '0': break
        elif user['role'] == 'user':
            menu_user()
            choice = input("Выберите действие: ")
            if choice == '0': break

if __name__ == '__main__':
    main()
