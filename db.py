import json
import os
from abc import ABC, abstractmethod

from models import Book, BookStatus


class AbstractDBConnector(ABC):
    """
    Абстрактный класс для подключения к базе данных.
    """

    @abstractmethod
    def add_book(self, book):
        """
        Добавить новую книгу в базу данных.
        :param book: Добавляемая книга
        """
        pass

    @abstractmethod
    def remove_book(self, book_pk: int):
        """
        Удалить книгу по идентификатору из базы данных.
        :param book_pk: Идентификатор удаляемой книги
        """
        pass

    @abstractmethod
    def search_books(
        self, title: str = "", author: str = "", year: int = 0
    ) -> list[Book]:
        """
        Поиск книг по заголовку, автору и году издания.
        :param title: Заголовок книги
        :param author: Автор книги
        :param year: Год издания книги
        :return: Список найденных книг
        """
        pass

    @abstractmethod
    def update_book_status(self, book_pk: int, new_status: BookStatus):
        """
        Обновить статус книги по идентификатору в базе данных.
        :param book_pk: Идентификатор книги
        :param new_status: Новый статус книги
        """
        pass

    @abstractmethod
    def list_books(self) -> list[Book]:
        """
        Получить список всех книг из базы данных.
        :return: Список всех книг
        """
        pass


class JsonDbConnector(AbstractDBConnector):
    """
    Класс для работы с базой данных через JSON-файл.
    """

    def __init__(self, filename: str):
        self.filename = filename

    def __load_data(self) -> list[Book]:
        if not os.path.exists(self.filename):
            return []

        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return [Book(**item) for item in data]

    def __get_next_unique_pk(self):
        if not os.path.exists(self.filename):
            return 1

        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return max(item[Book.pk.fget.__name__] for item in data) + 1 if data else 1

    def __save_data(self, data: list[Book]):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([item.to_dict() for item in data], file, indent=4)

    def add_book(self, book: Book):
        book.pk = self.__get_next_unique_pk()
        self.__save_data([*self.__load_data(), book])

    def remove_book(self, book_pk: int):
        data = self.__load_data()
        self.__save_data([item for item in data if item.pk != book_pk])

    def search_books(
        self, title: str = "", author: str = "", year: int = 0
    ) -> list[Book]:
        # Если поля поиска пусты, то в них поиск не проходит
        # В противном случае, поиск ведется через И
        def search_title(item_title: str, title: str) -> bool:
            if title:
                return item_title.lower().find(title) != -1
            return True

        def search_author(item_author: str, author: str) -> bool:
            if author:
                return item_author.lower().find(author) != -1
            return True

        def search_year(item_year: int, year: int) -> bool:
            if year:
                return item_year == year
            return True

        title = title.lower().strip()
        author = author.lower().strip()
        data = self.__load_data()
        return [
            item
            for item in data
            if (
                search_title(item.title, title)
                and search_author(item.author, author)
                and search_year(item.year, year)
            )
        ]

    def update_book_status(self, book_pk: int, new_status: BookStatus):
        data = self.__load_data()
        updated_data = [
            (
                item
                if item.pk != book_pk
                else Book(
                    pk=item.pk,
                    title=item.title,
                    year=item.year,
                    author=item.author,
                    status=new_status,
                )
            )
            for item in data
        ]
        self.__save_data(updated_data)

    def list_books(self) -> list[Book]:
        return self.__load_data()
