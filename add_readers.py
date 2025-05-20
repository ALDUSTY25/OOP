# add_readers.py
from app import app, db
from models import Reader
from werkzeug.security import generate_password_hash

with app.app_context():
    readers_data = [
        {"username": "ivan123", "password": "pass123"},
        {"username": "anna_reader", "password": "secure456"},
    ]

    for data in readers_data:
        existing_reader = Reader.query.filter_by(username=data['username']).first()
        if not existing_reader:
            new_reader = Reader(
                username=data['username'],
                password=generate_password_hash(data['password'])
            )
            db.session.add(new_reader)
            print(f"Добавлен читатель: {data['username']}")  # Для отладки

    db.session.commit()
    print("✅ Читатели успешно добавлены.")