# Импортируем объект базы данных из __init__.py
from . import db
# Импортируем UserMixin — специальный миксин для поддержки Flask-Login
from flask_login import UserMixin

# Определяем модель пользователя для хранения в базе данных
class User(db.Model, UserMixin):
    # Имя таблицы в базе данных
    __tablename__ = 'users'
    # Уникальный идентификатор пользователя (первичный ключ)
    id = db.Column(db.Integer, primary_key=True)
    # Имя пользователя (уникальное, не может быть пустым)
    username = db.Column(db.String(150), unique=True, nullable=False)
    # Хэш пароля пользователя (не храните пароли в открытом виде!)
    password = db.Column(db.String(256), nullable=False)

    # Метод __repr__ нужен для отладки, чтобы видеть объекты пользователя в консоли
    def __repr__(self):
        return f'<User {self.username}>'
