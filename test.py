import unittest
from models import Book, BookStatus


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


if __name__ == "__main__":
    unittest.main()
