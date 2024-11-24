from enum import Enum


class BookStatus(Enum):
    """
    Перечисление, представляющее статус книги.
    """

    AVAILABLE = "1"
    ISSUED = "2"


class Book:
    """
    Класс, представляющий модель книги.
    """

    def __init__(
        self,
        title: str,
        author: str,
        year: int,
        status: BookStatus | str = BookStatus.AVAILABLE,
        pk: int = 0,
    ):
        self.__pk = pk
        self.__title = title.strip()
        self.__author = author.strip()
        self.__year = year

        if isinstance(status, BookStatus):
            self.__status = status
        elif isinstance(status, str):
            self.__status = BookStatus(status)
        else:
            raise ValueError("Invalid status type")

    @property
    def pk(self) -> int:
        return self.__pk

    @pk.setter
    def pk(self, new_pk: int):
        self.__pk = new_pk

    @property
    def title(self) -> str:
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
        """
        Метод, возвращающий словарь с данными о книге.
        """
        # self.__class__.PROPERTY.fget.__name__ - получение имени свойства в виде строки
        return {
            self.__class__.pk.fget.__name__: self.pk,
            self.__class__.title.fget.__name__: self.title,
            self.__class__.author.fget.__name__: self.author,
            self.__class__.year.fget.__name__: self.year,
            self.__class__.status.fget.__name__: self.status.value,
        }

    def __str__(self):
        return (
            f"{self.pk}: {self.title}, {self.author}, {self.year} | {self.status.name}"
        )
