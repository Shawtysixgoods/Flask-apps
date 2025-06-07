# Импортируем необходимые модули из стандартной библиотеки Python и Flask
# Flask — основной класс для создания приложения
from flask import Flask, render_template, request, redirect, url_for, flash
# Flask-SQLAlchemy — расширение для интеграции SQLAlchemy с Flask
# Документация: https://flask-sqlalchemy.palletsprojects.com/
from flask_sqlalchemy import SQLAlchemy
# datetime — модуль для работы с датой и временем
from datetime import datetime

# Создаём экземпляр Flask-приложения
app = Flask(__name__)
# Устанавливаем секретный ключ, необходимый для работы flash-сообщений и защиты от CSRF-атак
app.config['SECRET_KEY'] = 'очень_секретный_ключ'
# Указываем строку подключения к базе данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messanger.db'
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
    # messages_sent — связь с отправленными сообщениями (один-ко-многим)
    messages_sent = db.relationship('Message', backref='sender', foreign_keys='Message.sender_id', lazy=True)
    # messages_received — связь с полученными сообщениями (один-ко-многим)
    messages_received = db.relationship('Message', backref='recipient', foreign_keys='Message.recipient_id', lazy=True)

    def __repr__(self):
        return f'<User {self.id} {self.username}>'

# Определяем модель сообщения (Message)
class Message(db.Model):
    __tablename__ = 'messages'
    # id — первичный ключ, уникальный идентификатор сообщения
    id = db.Column(db.Integer, primary_key=True)
    # sender_id — внешний ключ на пользователя-отправителя
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # recipient_id — внешний ключ на пользователя-получателя
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # content — содержимое сообщения, не может быть пустым
    content = db.Column(db.Text, nullable=False)
    # timestamp — дата и время отправки сообщения
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Message {self.id}>'

# Главная страница: список всех пользователей
@app.route('/')
def index():
    # Получаем всех пользователей из базы данных
    users = User.query.all()
    # Передаём список пользователей в шаблон
    return render_template('index.html', users=users)

# Страница регистрации нового пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            flash('Имя пользователя обязательно!')
            return redirect(url_for('register'))
        # Проверяем, что имя пользователя уникально
        if User.query.filter_by(username=username).first():
            flash('Пользователь с таким именем уже существует!')
            return redirect(url_for('register'))
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        flash('Пользователь зарегистрирован!')
        return redirect(url_for('index'))
    return render_template('register.html')

# Страница просмотра диалога между двумя пользователями
@app.route('/dialog/<int:user1_id>/<int:user2_id>', methods=['GET', 'POST'])
def dialog(user1_id, user2_id):
    # Получаем пользователей по id
    user1 = User.query.get_or_404(user1_id)
    user2 = User.query.get_or_404(user2_id)
    # Если отправлено новое сообщение
    if request.method == 'POST':
        content = request.form.get('content')
        if not content:
            flash('Сообщение не может быть пустым!')
            return redirect(url_for('dialog', user1_id=user1_id, user2_id=user2_id))
        message = Message(sender_id=user1.id, recipient_id=user2.id, content=content)
        db.session.add(message)
        db.session.commit()
        flash('Сообщение отправлено!')
        return redirect(url_for('dialog', user1_id=user1_id, user2_id=user2_id))
    # Получаем все сообщения между двумя пользователями (в обе стороны), сортируем по времени
    messages = Message.query.filter(
        ((Message.sender_id == user1.id) & (Message.recipient_id == user2.id)) |
        ((Message.sender_id == user2.id) & (Message.recipient_id == user1.id))
    ).order_by(Message.timestamp).all()
    return render_template('dialog.html', user1=user1, user2=user2, messages=messages)

# Запуск приложения только если файл запущен напрямую
if __name__ == '__main__':
    # Создаём все таблицы в базе данных, если их ещё нет
    db.create_all()
    # app.run() запускает встроенный сервер Flask
    # debug=True включает режим отладки (не использовать в продакшене)
    app.run(debug=True)
