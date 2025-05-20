from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))  # Название
    year = db.Column(db.Integer)       # Год выпуска
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))  # Автор
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))    # Жанр
    cover = db.Column(db.String(200))  # Путь к обложке

    author = db.relationship("Author", backref="books")
    genre = db.relationship("Genre", backref="books")

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))  # Имя автора

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))  # Название жанра

class Reader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)   # Логин
    password = db.Column(db.String(100))                # Пароль
    is_admin = db.Column(db.Boolean, default=False)     # Флаг администратора