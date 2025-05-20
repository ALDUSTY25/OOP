from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from forms import BookForm, RegisterForm, AuthorForm
from models import db, Book, Author, Genre, Reader, User
from decorators import admin_required
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.normpath(os.path.join('static', 'covers'))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
app.config['WTF_CSRF_ENABLED']= False

# �������� ����� covers, ���� � ���
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
csrf = CSRFProtect(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/books')
def books():
    all_books = Book.query.all()
    return render_template('books.html', books=all_books)


@app.route('/add_book', methods=['GET', 'POST'])
@admin_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        cover_path = None

        if form.cover.data:
            cover_file = form.cover.data
            cover_filename = secure_filename(cover_file.filename)
            cover_path = os.path.join('covers', cover_filename)  # ��������� ������ covers/filename.jpg
            cover_file.save(os.path.join(app.config['UPLOAD_FOLDER'], cover_filename))

        author = Author.query.filter_by(name=form.author_name.data).first()
        if not author:
            author = Author(name=form.author_name.data)
            db.session.add(author)

        genre = Genre.query.filter_by(name=form.genre_name.data).first()
        if not genre:
            genre = Genre(name=form.genre_name.data)
            db.session.add(genre)

        db.session.commit()

        new_book = Book(
            title=form.title.data,
            year=form.year.data,
            author_id=author.id,
            genre_id=genre.id,
            cover=cover_path  # ��������� ������ ������������� ����
        )
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('books'))

    return render_template('add_book.html', form=form)


@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@admin_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)

    if request.method == 'POST':
        if form.validate_on_submit():
            book.title = form.title.data
            book.year = form.year.data

            author = Author.query.filter_by(name=form.author_name.data).first()
            if not author:
                author = Author(name=form.author_name.data)
                db.session.add(author)

            genre = Genre.query.filter_by(name=form.genre_name.data).first()
            if not genre:
                genre = Genre(name=form.genre_name.data)
                db.session.add(genre)

            # ���������� �������
            if form.cover.data:
                cover_file = form.cover.data
                cover_filename = secure_filename(cover_file.filename)
                cover_path = os.path.join('covers', cover_filename)
                cover_file.save(os.path.join(app.config['UPLOAD_FOLDER'], cover_filename))
                book.cover = cover_path

            db.session.commit()
            return redirect(url_for('books'))

    return render_template('edit_book.html', form=form, book=book)


@app.route('/authors')
def authors():
    return render_template('authors.html', authors=Author.query.all())


@app.route('/authors/edit/<int:author_id>', methods=['GET', 'POST'])
def edit_author(author_id):
    author = Author.query.get_or_404(author_id)
    form = AuthorForm(obj=author)

    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(author)
            db.session.commit()
            return redirect(url_for('authors'))

    return render_template('edit_author.html', form=form, author=author)


@app.route('/genres')
def genres():
    return render_template('genres.html', genres=Genre.query.all())


@app.route('/genre/<int:genre_id>')
def genre_detail(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    books = Book.query.filter_by(genre_id=genre_id).all()
    return render_template('genre_detail.html', genre=genre, books=books)


@app.route('/readers')
def readers():
    return render_template('readers.html', readers=Reader.query.all())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            password=form.password.data,
            is_admin=form.is_admin.data
        )
        db.session.add(new_user)
        db.session.commit()

        # ��������� ������������ ��� ��������
        new_reader = Reader(
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(new_reader)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/add_reader')
def add_reader():
    try:
        new_reader = Reader(
            username="ivan123",
            password="pass123"
        )
        db.session.add(new_reader)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("error:", e)

    return redirect(url_for('readers'))


def open_browser():
    import webbrowser
    webbrowser.open_new("http://127.0.0.1:5000/")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, app, use_reloader=True, use_debugger=True, threaded=True)