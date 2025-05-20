from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))  # ��������
    year = db.Column(db.Integer)       # ��� �������
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))  # �����
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))    # ����
    cover = db.Column(db.String(200))  # ���� � �������

    author = db.relationship("Author", backref="books")
    genre = db.relationship("Genre", backref="books")

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))  # ��� ������

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))  # �������� �����

class Reader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)   # �����
    password = db.Column(db.String(100))                # ������
    is_admin = db.Column(db.Boolean, default=False)     # ���� ��������������