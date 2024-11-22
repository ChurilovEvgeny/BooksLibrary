from enum import Enum


class BookStatus(Enum):
    AVAILABLE = 1
    ISSUED = 2


class Book:
    def __init__(self, id: int, title: str, author: str, year: int, status: BookStatus):
        self.__id = id
        self.__title = title.strip()
        self.__author = author.strip()
        self.__year = year
        self.__status = status

    @property
    def id(self) -> int:
        return self.__id

    @property
    def title(self):
        return self.__title

    @property
    def author(self) -> str:
        return self.__author

    @property
    def year(self) -> int:
        return self.__year

    @property
    def status(self) -> BookStatus:
        return self.__status

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status.value
        }

    def __str__(self):
        return f"{self.id}: {self.title}, {self.author}, {self.year} | {self.status}"
