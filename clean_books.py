# -*- coding: utf-8 -*-
from app import app, db
from models import Book

with app.app_context():
    seen = set()       # Множество для отслеживания уникальных книг
    duplicates = []    # Список для хранения найденных дубликатов

    # Перебор всех книг в базе
    for book in Book.query.all():
        key = (book.title.lower(), book.year)  # Ключ = название (в нижнем регистре) + год
        if key in seen:
            duplicates.append(book)  # Если уже есть такая книга — это дубликат
        else:
            seen.add(key)  # Иначе — добавляем в множество уникальных

    # Удаление дубликатов из базы
    for dup in duplicates:
        db.session.delete(dup)

    db.session.commit()  # Сохраняем изменения
    print(f"Удалено повторяющихся книг: {len(duplicates)}")  # Выводим результат

