# Импортируем необходимые модули из стандартной библиотеки Python и Flask
# Flask — основной класс для создания приложения
from flask import Flask
# Flask-SQLAlchemy — расширение для интеграции SQLAlchemy с Flask
# Документация: https://flask-sqlalchemy.palletsprojects.com/
from flask_sqlalchemy import SQLAlchemy
# Flask-Admin — расширение для создания административных интерфейсов
# Документация: https://flask-admin.readthedocs.io/
from flask_admin import Admin
# Импортируем ModelView для отображения моделей в админке
from flask_admin.contrib.sqla import ModelView

# Создаём экземпляр Flask-приложения
app = Flask(__name__)
# Устанавливаем секретный ключ, необходимый для работы сессий и защиты от CSRF-атак
app.config['SECRET_KEY'] = 'очень_секретный_ключ'
# Указываем строку подключения к базе данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin_example.db'
# Отключаем отслеживание изменений объектов для экономии памяти
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Создаём экземпляр SQLAlchemy для работы с базой данных
# db — объект для взаимодействия с БД
# Документация: https://flask-sqlalchemy.palletsprojects.com/en/latest/api/
db = SQLAlchemy(app)

# Определяем модель User для примера
# Класс наследует db.Model — базовый класс для всех моделей SQLAlchemy
class User(db.Model):
    # Имя таблицы в базе данных (по умолчанию — имя класса в нижнем регистре)
    __tablename__ = 'users'
    # id — первичный ключ, уникальный идентификатор пользователя
    id = db.Column(db.Integer, primary_key=True)
    # name — строковое поле для имени пользователя, не может быть пустым
    name = db.Column(db.String(50), nullable=False)
    # email — строковое поле для email, не может быть пустым и должен быть уникальным
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Метод __repr__ нужен для отладки, чтобы удобно выводить объекты
    def __repr__(self):
        return f'<User {self.id} {self.name}>'

# Создаём экземпляр Flask-Admin
# Документация: https://flask-admin.readthedocs.io/en/latest/introduction/
admin = Admin(app, name='Пример Flask-Admin', template_mode='bootstrap4')
# Регистрируем модель User в административном интерфейсе
# ModelView — стандартное представление для моделей SQLAlchemy
admin.add_view(ModelView(User, db.session))

# Главная страница (опционально)
@app.route('/')
def index():
    # Простая страница с ссылкой на админку
    return '<h1>Главная страница</h1><p><a href="/admin/">Перейти в админку</a></p>'

# Запуск приложения только если файл запущен напрямую
if __name__ == '__main__':
    # Создаём все таблицы в базе данных, если их ещё нет
    db.create_all()
    # app.run() запускает встроенный сервер Flask
    # debug=True включает режим отладки (не использовать в продакшене)
    app.run(debug=True)
