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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
# Отключаем отслеживание изменений объектов для экономии памяти
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Создаём экземпляр SQLAlchemy для работы с базой данных
# db — объект для взаимодействия с БД
# Документация: https://flask-sqlalchemy.palletsprojects.com/en/latest/api/
db = SQLAlchemy(app)

# Определяем модель пользователя (User)
class User(db.Model):
    # Имя таблицы в базе данных
    __tablename__ = 'users'
    # id — первичный ключ, уникальный идентификатор пользователя
    id = db.Column(db.Integer, primary_key=True)
    # username — строковое поле для имени пользователя, не может быть пустым и должен быть уникальным
    username = db.Column(db.String(50), unique=True, nullable=False)
    # posts — связь с постами (один-ко-многим)
    posts = db.relationship('Post', backref='author', lazy=True)
    # comments — связь с комментариями (один-ко-многим)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.id} {self.username}>'

# Определяем модель темы (Topic)
class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    # title — название темы, не может быть пустым
    title = db.Column(db.String(100), nullable=False)
    # posts — связь с постами (один-ко-многим)
    posts = db.relationship('Post', backref='topic', lazy=True)

    def __repr__(self):
        return f'<Topic {self.id} {self.title}>'

# Определяем модель поста (Post)
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    # content — содержимое поста, не может быть пустым
    content = db.Column(db.Text, nullable=False)
    # user_id — внешний ключ на пользователя
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # topic_id — внешний ключ на тему
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    # comments — связь с комментариями (один-ко-многим)
    comments = db.relationship('Comment', backref='post', lazy=True)

    def __repr__(self):
        return f'<Post {self.id}>'

# Определяем модель комментария (Comment)
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    # content — содержимое комментария, не может быть пустым
    content = db.Column(db.Text, nullable=False)
    # user_id — внешний ключ на пользователя
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # post_id — внешний ключ на пост
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def __repr__(self):
        return f'<Comment {self.id}>'

# Главная страница: список всех тем форума
@app.route('/')
def index():
    # Получаем все темы из базы данных
    topics = Topic.query.all()
    # Передаём список тем в шаблон
    return render_template('index.html', topics=topics)

# Страница темы: список всех постов в теме
@app.route('/topic/<int:topic_id>')
def topic_detail(topic_id):
    # Получаем тему по id или возвращаем 404, если не найдено
    topic = Topic.query.get_or_404(topic_id)
    # Получаем все посты в теме
    posts = Post.query.filter_by(topic_id=topic.id).all()
    return render_template('topic.html', topic=topic, posts=posts)

# Страница поста: просмотр поста и комментариев
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    # Получаем пост по id или возвращаем 404
    post = Post.query.get_or_404(post_id)
    # Получаем все комментарии к посту
    comments = Comment.query.filter_by(post_id=post.id).all()
    if request.method == 'POST':
        # Получаем имя пользователя и текст комментария из формы
        username = request.form.get('username')
        content = request.form.get('content')
        # Проверяем, что поля не пустые
        if not username or not content:
            flash('Все поля обязательны для заполнения!')
            return redirect(url_for('post_detail', post_id=post.id))
        # Находим или создаём пользователя
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        # Создаём комментарий
        comment = Comment(content=content, user_id=user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Комментарий добавлен!')
        return redirect(url_for('post_detail', post_id=post.id))
    return render_template('post.html', post=post, comments=comments)

# Создание новой темы
@app.route('/new_topic', methods=['GET', 'POST'])
def new_topic():
    if request.method == 'POST':
        title = request.form.get('title')
        if not title:
            flash('Название темы обязательно!')
            return redirect(url_for('new_topic'))
        topic = Topic(title=title)
        db.session.add(topic)
        db.session.commit()
        flash('Тема создана!')
        return redirect(url_for('index'))
    return render_template('new_topic.html')

# Создание нового поста в теме
@app.route('/topic/<int:topic_id>/new_post', methods=['GET', 'POST'])
def new_post(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    if request.method == 'POST':
        username = request.form.get('username')
        content = request.form.get('content')
        if not username or not content:
            flash('Все поля обязательны для заполнения!')
            return redirect(url_for('new_post', topic_id=topic.id))
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        post = Post(content=content, user_id=user.id, topic_id=topic.id)
        db.session.add(post)
        db.session.commit()
        flash('Пост добавлен!')
        return redirect(url_for('topic_detail', topic_id=topic.id))
    return render_template('new_post.html', topic=topic)

# Запуск приложения только если файл запущен напрямую
if __name__ == '__main__':
    # Создаём все таблицы в базе данных, если их ещё нет
    db.create_all()
    # app.run() запускает встроенный сервер Flask
    # debug=True включает режим отладки (не использовать в продакшене)
    app.run(debug=True)
