# Импортируем основной класс Flask для создания приложения
from flask import Flask

# Импортируем расширение Flask-WTF для поддержки форм
# Документация: https://flask-wtf.readthedocs.io/en/stable/
from flask_wtf import CSRFProtect  # Для защиты форм от CSRF-атак

def create_app():
    # Создаём экземпляр приложения Flask
    app = Flask(__name__)
    # Устанавливаем секретный ключ, необходимый для работы сессий, CSRF и Flask-WTF
    app.config['SECRET_KEY'] = 'your_secret_key'  # В реальных проектах используйте переменные окружения!

    # Инициализируем защиту от CSRF-атак для всех форм в приложении
    # Подробнее: https://flask-wtf.readthedocs.io/en/stable/csrf.html
    csrf = CSRFProtect(app)

    # Импортируем и регистрируем blueprint с маршрутами
    from .routes import wtf_bp
    app.register_blueprint(wtf_bp)

    # Возвращаем готовое приложение
    return app
