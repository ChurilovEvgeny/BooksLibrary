import json
import os

from models import Book, BookStatus


class DbConnector:
    def __init__(self, filename: str):
        self.filename = filename

    def load_data(self) -> list[Book]:
        if not os.path.exists(self.filename):
            return []

        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return [Book(**item) for item in data]

    def get_next_unique_id(self):
        if not os.path.exists(self.filename):
            return 1

        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return max(item["id"] for item in data) + 1 if data else 1

    def save_data(self, data: list[Book]):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([item.to_dict() for item in data], file, indent=4)

    def add_book(self, book: Book):
        self.save_data([*self.load_data(), book])

    def remove_book(self, book_id: int):
        data = self.load_data()
        self.save_data([item for item in data if item.id != book_id])

    def search_book(self, title: str = "", author: str = "", year: int = 0):
        title = title.lower().strip()
        author = author.lower().strip()
        data = self.load_data()
        return [item for item in data if
                (title and item.title.lower() == title) and
                (author and item.author.lower() == author) and
                (year and item.year == year)]

    def update_book_status(self, book_id: int, new_status: BookStatus):
        data = self.load_data()
        updated_data = [
            item if item.id != book_id
            else Book(id=item.id, title=item.title, year=item.year, author=item.author, status=new_status)
            for item in data
        ]
        self.save_data(updated_data)