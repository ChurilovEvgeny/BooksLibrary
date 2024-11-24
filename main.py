from enum import Enum

from db import DbConnector
from models import Book, BookStatus


class BookCommands(Enum):
    # Enum строковых констант, чтобы не было проблем с преобразованием типов
    EXIT = "0"

    ADD = "1"
    REMOVE = "2"
    UPDATE = "3"
    LIST = "4"


class ProgramMenu:
    def __init__(self, db_connector):
        self.db_connector = db_connector  # подключение к БД
        self.run_menu()  # запуск меню

    def run_menu(self):
        while True:
            command = input(
                "Введите номер команды:\n"
                + f"{BookCommands.ADD.value} - добавить\n"
                + f"{BookCommands.REMOVE.value} - удалить\n"
                + f"{BookCommands.UPDATE.value} - обновить статус\n"
                + f"{BookCommands.LIST.value} - список все книг\n"
                + f"{BookCommands.EXIT.value} - выход\n: "
            ).strip()

            if command == BookCommands.ADD.value:
                self.add_book()
            elif command == BookCommands.REMOVE.value:
                self.remove_book()
            elif command == BookCommands.UPDATE.value:
                self.update_book()
            elif command == BookCommands.LIST.value:
                self.list_books()
            elif command == BookCommands.EXIT.value:
                break
            else:
                print("Неизвестная команда. Попробуйте снова.")

    def add_book(self):
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        while True:
            year = input("Введите год издания книги: ")
            if not year.isdigit():
                print("Введён некорректный год. Попробуйте снова.")

            year = int(year)
            break

        book = Book(title=title, author=author, year=year)
        self.db_connector.add_book(book)
        print("Книга добавлена!")

    def remove_book(self):
        while True:
            book_pk = input("Введите PK книги для удаления: ")
            if not book_pk.isdigit():
                print("Введён некорректный PK. Попробуйте снова.")

            book_pk = int(book_pk)
            break

        self.db_connector.remove_book(book_pk)
        print("Книга удалена!")

    def update_book(self):
        while True:
            book_pk = input("Введите PK книги для изменения статуса: ")
            if book_pk.isdigit():
                book_pk = int(book_pk)
                break
            else:
                print("Введён некорректный PK. Попробуйте снова.")

        while True:
            status = input(
                "Введите новый статус:\n"
                + f"{BookStatus.AVAILABLE.value} - в наличии\n"
                + f"{BookStatus.ISSUED.value} - выдана\n: "
            ).strip()

            if status in (BookStatus.AVAILABLE.value, BookStatus.ISSUED.value):
                self.db_connector.update_book_status(book_pk=book_pk, new_status=status)
                print("Статус обновлён!")
                break
            else:
                print("Неизвестный статус. Попробуйте снова.")

    def list_books(self):
        books = self.db_connector.list_books()
        if books:
            for book in books:
                print(book)
        else:
            print("Список книг пуст.")


def main():
    db_connector = DbConnector("books.json")
    ProgramMenu(db_connector)


if __name__ == "__main__":
    main()
