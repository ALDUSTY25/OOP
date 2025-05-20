# -*- coding: utf-8 -*-

from app import app, db
from models import Author, Genre, Book

with app.app_context():
    db.create_all()

    # Добавим жанры
    genres = [
        Genre(name="Фантастика"),
        Genre(name="Фэнтези"),
        Genre(name="Детектив"),
        Genre(name="Роман"),
        Genre(name="Приключения")
    ]
    db.session.add_all(genres)

    # Добавим авторов
    authors = [
        Author(name="Джордж Оруэлл"),
        Author(name="Фёдор Достоевский"),
        Author(name="Дж. Р. Р. Толкин"),
        Author(name="Артур Конан Дойл"),
        Author(name="Лев Толстой")
    ]
    db.session.add_all(authors)
    db.session.commit()

    # Добавим книги
    books = [
        Book(title="1984", year=1949, author_id=1, genre_id=1),
        Book(title="Преступление и наказание", year=1866, author_id=2, genre_id=4),
        Book(title="Властелин колец", year=1954, author_id=3, genre_id=2),
        Book(title="Шерлок Холмс", year=1892, author_id=4, genre_id=3),
        Book(title="Война и мир", year=1869, author_id=5, genre_id=4),
        Book(title="Скотный двор", year=1945, author_id=1, genre_id=1),
        Book(title="Идиот", year=1869, author_id=2, genre_id=4),
        Book(title="Хоббит", year=1937, author_id=3, genre_id=2),
        Book(title="Знак четырёх", year=1890, author_id=4, genre_id=3),
        Book(title="Анна Каренина", year=1877, author_id=5, genre_id=4),
        Book(title="На маяк", year=1927, author_id=1, genre_id=4),
        Book(title="Игрок", year=1867, author_id=2, genre_id=4),
        Book(title="Сильмариллион", year=1977, author_id=3, genre_id=2),
        Book(title="Пёс Баскервилей", year=1902, author_id=4, genre_id=3),
        Book(title="Детство", year=1852, author_id=5, genre_id=4),
        Book(title="1985", year=2020, author_id=1, genre_id=1),
        Book(title="Бесы", year=1872, author_id=2, genre_id=4),
        Book(title="Две крепости", year=1954, author_id=3, genre_id=2),
        Book(title="Этюд в багровых тонах", year=1887, author_id=4, genre_id=3),
        Book(title="Казаки", year=1863, author_id=5, genre_id=5),
    ]
    db.session.add_all(books)
    db.session.commit()
    print("База данных создана и заполнена.")
