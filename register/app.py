# Импорт необходимых модулей
from flask import Flask, render_template, redirect, url_for, flash  # Flask - веб-фреймворк
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy - ORM для работы с БД
from flask_wtf import FlaskForm  # FlaskForm - базовый класс для форм
from wtforms import StringField, PasswordField, SubmitField  # Поля формы
from wtforms.validators import DataRequired, Length, EqualTo  # Валидаторы полей
from werkzeug.security import generate_password_hash  # Для хеширования паролей

# Создание Flask-приложения
app = Flask(__name__)

# Конфигурация приложения
app.config['SECRET_KEY'] = 'ваш-секретный-ключ'  # Ключ для защиты от CSRF
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Путь к SQLite базе
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем уведомления об изменениях

# Инициализация SQLAlchemy
db = SQLAlchemy(app)

## Модель пользователя для базы данных
class User(db.Model):
    # Уникальный идентификатор пользователя (первичный ключ)
    id = db.Column(db.Integer, primary_key=True)
    
    # Имя пользователя (должно быть уникальным)
    username = db.Column(db.String(50), unique=True, nullable=False)
    
    # Хеш пароля (не может быть пустым)
    password = db.Column(db.String(100), nullable=False)

    # Метод для отображения объекта при выводе
    def __repr__(self):
        return f'<User {self.username}>'

## Форма регистрации
class RegistrationForm(FlaskForm):
    # Поле для ввода имени пользователя
    username = StringField(
        'Логин',
        validators=[
            DataRequired(message='Обязательное поле'),  # Поле обязательно для заполнения
            Length(min=4, max=20, message='Длина от 4 до 20 символов')  # Ограничение длины
        ]
    )
    
    # Поле для ввода пароля
    password = PasswordField(
        'Пароль',
        validators=[
            DataRequired(message='Обязательное поле'),  # Поле обязательно для заполнения
            Length(min=6, message='Минимум 6 символов')  # Минимальная длина
        ]
    )
    
    # Поле для подтверждения пароля
    confirm_password = PasswordField(
        'Повторите пароль',
        validators=[
            DataRequired(message='Обязательное поле'),  # Поле обязательно для заполнения
            EqualTo('password', message='Пароли должны совпадать')  # Должно совпадать с password
        ]
    )
    
    # Кнопка отправки формы
    submit = SubmitField('Зарегистрироваться')

# Создание таблиц в базе данных перед первым запросом
@app.before_first_request
def create_tables():
    db.create_all()  # Создает все таблицы, определенные в моделях

## Главная страница
@app.route('/')
def home():
    # Простое приветствие со ссылкой на регистрацию
    return 'Добро пожаловать! <a href="/register">Зарегистрироваться</a>'

## Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Создаем экземпляр формы
    form = RegistrationForm()
    
    # Если форма отправлена и прошла валидацию
    if form.validate_on_submit():
        try:
            # Хешируем пароль перед сохранением
            hashed_password = generate_password_hash(form.password.data)
            
            # Создаем нового пользователя
            user = User(username=form.username.data, password=hashed_password)
            
            # Добавляем пользователя в сессию
            db.session.add(user)
            
            # Сохраняем изменения в базе
            db.session.commit()
            
            # Показываем сообщение об успехе
            flash('Регистрация прошла успешно!', 'success')
            
            # Перенаправляем на главную
            return redirect(url_for('home'))
        except:
            # В случае ошибки откатываем изменения
            db.session.rollback()
            flash('Ошибка при регистрации', 'error')
    
    # Рендерим шаблон с формой (GET запрос или форма не прошла валидацию)
    return render_template('register.html', form=form)

# Точка входа - запуск приложения
if __name__ == '__main__':
    app.run(debug=True)  # Запуск с включенным режимом отладки