from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

class BookForm(FlaskForm):
    title = StringField('Название')
    year = IntegerField('Год')
    author_name = StringField('Автор')
    genre_name = StringField('Жанр')
    cover = FileField('Обложка', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Только изображения!')])
    submit = SubmitField('Сохранить')                           # Кнопка отправки формы

class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3)])  # Логин
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=4)])          # Пароль
    is_admin = BooleanField('Администратор')                                                 # Чекбокс "админ"
    submit = SubmitField('Зарегистрироваться')                                               # Кнопка

class AuthorForm(FlaskForm):
    name = StringField('Имя автора', validators=[DataRequired()])
