# Импортируем необходимые модули Flask
from flask import Flask  # Основной класс приложения Flask
from flask_sqlalchemy import SQLAlchemy  # Расширение для работы с базой данных через ORM
from flask_login import LoginManager  # Расширение для управления сессиями пользователей

# Создаём экземпляр SQLAlchemy для работы с базой данных
db = SQLAlchemy()
# Создаём экземпляр LoginManager для управления авторизацией пользователей
login_manager = LoginManager()

def create_app():
    # Создаём экземпляр приложения Flask
    app = Flask(__name__)
    # Устанавливаем секретный ключ для защиты cookies и сессий (обязательно для безопасности)
    app.config['SECRET_KEY'] = 'your_secret_key'  # В реальных проектах используйте переменные окружения!
    # Указываем строку подключения к базе данных SQLite (можно заменить на другую СУБД)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    # Инициализируем расширения с приложением
    db.init_app(app)
    login_manager.init_app(app)
    # Указываем, куда перенаправлять неавторизованных пользователей при попытке доступа к защищённым маршрутам
    login_manager.login_view = 'login.login'
    # Импортируем и регистрируем blueprint с маршрутами аутентификации
    from .routes import auth_bp
    app.register_blueprint(auth_bp)
    # Возвращаем готовое приложение
    return app
