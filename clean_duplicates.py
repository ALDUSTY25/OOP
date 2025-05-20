# -*- coding: utf-8 -*-
from app import app, db
from models import Author, Genre

with app.app_context():
    def delete_duplicates(model):
        seen = set()        # Множество уникальных имён
        duplicates = []     # Список для дубликатов

        # Перебираем все записи указанной модели (Author или Genre)
        for item in model.query.all():
            if item.name.lower() in seen:
                duplicates.append(item)  # Найден дубликат по имени
            else:
                seen.add(item.name.lower())  # Добавляем уникальное имя

        # Удаляем все дубликаты из базы
        for dup in duplicates:
            db.session.delete(dup)

        db.session.commit()  # Сохраняем изменения
        print(f"Удалено повторов: {len(duplicates)}")

    # Запускаем удаление дубликатов для авторов и жанров
    delete_duplicates(Author)
    delete_duplicates(Genre)

