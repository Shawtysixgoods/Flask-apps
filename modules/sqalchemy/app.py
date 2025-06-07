# Импортируем необходимые модули из стандартной библиотеки Python и Flask
# Flask — основной класс для создания приложения
from flask import Flask, render_template, request, redirect, url_for, flash
# Flask-SQLAlchemy — расширение для интеграции SQLAlchemy с Flask
# Документация: https://flask-sqlalchemy.palletsprojects.com/
from flask_sqlalchemy import SQLAlchemy

# Создаём экземпляр Flask-приложения
app = Flask(__name__)
# Устанавливаем секретный ключ, необходимый для работы flash-сообщений и защиты от CSRF-атак
app.config['SECRET_KEY'] = 'очень_секретный_ключ'
# Указываем строку подключения к базе данных SQLite
# Подробнее: https://flask-sqlalchemy.palletsprojects.com/en/latest/config/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
# Отключаем отслеживание изменений объектов для экономии памяти (опционально)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Создаём экземпляр SQLAlchemy, передавая ему наше приложение
# db — объект для работы с базой данных
# Документация: https://flask-sqlalchemy.palletsprojects.com/en/latest/api/
db = SQLAlchemy(app)

# Определяем модель (таблицу) для хранения записей
# Класс наследует db.Model — базовый класс для всех моделей SQLAlchemy
class Post(db.Model):
    # Имя таблицы в базе данных (по умолчанию — имя класса в нижнем регистре)
    __tablename__ = 'posts'
    # id — первичный ключ, уникальный идентификатор записи
    id = db.Column(db.Integer, primary_key=True)
    # title — строковое поле для заголовка поста, не может быть пустым
    title = db.Column(db.String(100), nullable=False)
    # content — текстовое поле для содержимого поста, не может быть пустым
    content = db.Column(db.Text, nullable=False)

    # Метод __repr__ нужен для отладки, чтобы удобно выводить объекты
    def __repr__(self):
        return f'<Post {self.id} {self.title}>'

# Главная страница: вывод всех постов
@app.route('/')
def index():
    # Получаем все записи из таблицы Post
    posts = Post.query.all()
    # Передаём список постов в шаблон
    return render_template('index.html', posts=posts)

# Страница для создания нового поста
@app.route('/new', methods=['GET', 'POST'])
def new_post():
    # Если форма отправлена методом POST
    if request.method == 'POST':
        # Получаем данные из формы
        title = request.form.get('title')
        content = request.form.get('content')
        # Проверяем, что поля не пустые
        if not title or not content:
            flash('Все поля обязательны для заполнения!')
            return redirect(url_for('new_post'))
        # Создаём новый объект Post
        post = Post(title=title, content=content)
        # Добавляем объект в сессию базы данных
        db.session.add(post)
        # Сохраняем изменения в базе данных
        db.session.commit()
        flash('Пост успешно создан!')
        # После создания перенаправляем на главную страницу
        return redirect(url_for('index'))
    # Если GET-запрос — отображаем форму
    return render_template('new_post.html')

# Страница для просмотра отдельного поста по id
@app.route('/post/<int:post_id>')
def post_detail(post_id):
    # Получаем пост по id или возвращаем 404, если не найден
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

# Запуск приложения только если файл запущен напрямую
if __name__ == '__main__':
    # Создаём все таблицы в базе данных, если их ещё нет
    # db.create_all() — создаёт таблицы по определённым моделям
    # Подробнее: https://flask-sqlalchemy.palletsprojects.com/en/latest/api/#flask_sqlalchemy.SQLAlchemy.create_all
    db.create_all()
    # app.run() запускает встроенный сервер Flask
    # debug=True включает режим отладки (не использовать в продакшене)
    app.run(debug=True)
