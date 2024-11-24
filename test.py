import os
import unittest

from db import JsonDbConnector
from models import Book, BookStatus


# python -m unittest - запуск тестов
# coverage run --source='.' -m unittest - запуск проверки покрытия
# coverage report -m - получение отчета с пропущенными стрроками


class TestModel(unittest.TestCase):
    def test_book_model_initialization(self):
        book = Book(title="Дерсу Узала", author="Арсеньев", year=1936)
        self.assertEqual(book.pk, 0)
        self.assertEqual(book.title, "Дерсу Узала")
        self.assertEqual(book.author, "Арсеньев")
        self.assertEqual(book.year, 1936)
        self.assertEqual(book.status, BookStatus.AVAILABLE)

        book = Book(
            pk=123,
            title="Что делать?",
            author="Чернышевский",
            year=1985,
            status=BookStatus.ISSUED,
        )
        self.assertEqual(book.pk, 123)
        self.assertEqual(book.title, "Что делать?")
        self.assertEqual(book.author, "Чернышевский")
        self.assertEqual(book.year, 1985)
        self.assertEqual(book.status, BookStatus.ISSUED)

        book = Book(title=" ", author=" ", year=0, status="1")
        self.assertEqual(book.status, BookStatus.AVAILABLE)

        book = Book(title=" ", author=" ", year=0, status="2")
        self.assertEqual(book.status, BookStatus.ISSUED)

        with self.assertRaises(ValueError) as e:
            Book(title=" ", author=" ", year=0, status=1)

    def test_change_pk(self):
        book = Book(title="", author="", year=0, status="1")
        self.assertEqual(book.pk, 0)

        book.pk = 123
        self.assertEqual(book.pk, 123)

    def test_to_dict(self):
        book = Book(
            pk=123,
            title="Что делать?",
            author="Чернышевский",
            year=1985,
            status=BookStatus.ISSUED,
        )
        self.assertEqual(
            book.to_dict(),
            {
                "pk": 123,
                "title": "Что делать?",
                "author": "Чернышевский",
                "year": 1985,
                "status": "2",
            },
        )

    def test_str(self):
        book = Book(
            pk=123,
            title="Что делать?",
            author="Чернышевский",
            year=1985,
            status=BookStatus.ISSUED,
        )
        self.assertEqual(
            str(book),
            f"{book.pk}: {book.title}, {book.author}, {book.year} | {book.status.name}",
        )


class TestJsonDbConnector(unittest.TestCase):
    fileName = "test.json"

    def setUp(self):
        # Setup your test database here
        pass

    def tearDown(self):
        os.remove(self.fileName)

    def test_add_book(self):
        book1 = Book(title="Дерсу Узала", author="Арсеньев", year=1936)
        connector = JsonDbConnector(self.fileName)
        connector.add_book(book1)

        book2 = Book(title="В горах Сихотэ-Алиня", author="Арсеньев", year=1937)
        connector.add_book(book2)

        loaded_books = connector.list_books()
        self.assertEqual(len(loaded_books), 2)

        loaded_book = loaded_books[0]
        self.assertEqual(loaded_book.title, book1.title)
        self.assertEqual(loaded_book.author, book1.author)
        self.assertEqual(loaded_book.year, book1.year)

        loaded_book = loaded_books[1]
        self.assertEqual(loaded_book.title, book2.title)
        self.assertEqual(loaded_book.author, book2.author)
        self.assertEqual(loaded_book.year, book2.year)

    def test_remove_book(self):
        book = Book(title="Дерсу Узала", author="Арсеньев", year=1936)
        connector = JsonDbConnector(self.fileName)
        connector.add_book(book)

        connector.remove_book(book.pk)

        loaded_books = connector.list_books()
        self.assertEqual(len(loaded_books), 0)

    def test_update_book_status(self):
        book = Book(title="Дерсу Узала", author="Арсеньев", year=1936)
        connector = JsonDbConnector(self.fileName)
        connector.add_book(book)

        connector.update_book_status(book.pk, BookStatus.ISSUED)

        loaded_books = connector.list_books()
        loaded_book = loaded_books[0]
        self.assertEqual(loaded_book.status, BookStatus.ISSUED)

    def test_search(self):
        book1 = Book(title="Дерсу Узала", author="Арсеньев", year=1936)
        book2 = Book(title="Что делать?", author="Чернышевский", year=1985)
        book3 = Book(title="В горах Сихотэ-Алиня", author="Арсеньев", year=1936)

        connector = JsonDbConnector(self.fileName)
        connector.add_book(book1)
        connector.add_book(book2)
        connector.add_book(book3)

        loaded_books = connector.search_books(title="Дерсу Узала")
        self.assertEqual(len(loaded_books), 1)
        self.assertEqual(loaded_books[0].title, book1.title)

        loaded_books = connector.search_books(title="Дерсу Узала", author="Некрасов")
        self.assertEqual(len(loaded_books), 0)

        loaded_books = connector.search_books(
            title="Что делать?", author="Чернышевский", year=1985
        )
        self.assertEqual(len(loaded_books), 1)
        self.assertEqual(loaded_books[0].author, book2.author)

        loaded_books = connector.search_books(author="арсен")
        self.assertEqual(len(loaded_books), 2)


if __name__ == "__main__":
    unittest.main()
