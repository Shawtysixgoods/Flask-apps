# Flask-SQLAlchemy: Работа с базами данных в Flask

SQLAlchemy - это мощная ORM (Object-Relational Mapping) для Python, которая позволяет работать с базами данных как с Python-объектами. Flask-SQLAlchemy - это расширение для Flask, которое упрощает интеграцию SQLAlchemy в Flask-приложения.

## Основные понятия

1. **ORM** - технология, которая связывает базу данных с объектами в коде
2. **Модель** - класс Python, который представляет таблицу в базе данных
3. **Сессия** - временная зона взаимодействия с базой данных
4. **Миграции** - система управления изменениями структуры базы данных

## Установка необходимых пакетов

```bash
pip install flask flask-sqlalchemy
```

## Базовая настройка

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Создаем экземпляр Flask приложения
app = Flask(__name__)

# Конфигурация базы данных (SQLite в данном случае)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем уведомления об изменениях

# Создаем экземпляр SQLAlchemy
db = SQLAlchemy(app)

# Теперь можно создавать модели и работать с базой данных
```

## Создание моделей

Модель - это Python класс, который наследуется от `db.Model` и представляет таблицу в базе данных.

### Пример модели "Пользователь"

```python
class User(db.Model):
    # Имя таблицы (необязательно, по умолчанию будет имя класса в нижнем регистре)
    __tablename__ = 'users'
    
    # Поля таблицы
    id = db.Column(db.Integer, primary_key=True)  # Первичный ключ
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Связи с другими таблицами (пример)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    # Метод для красивого вывода объекта
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
```

### Пример модели "Статья"

```python
class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Внешний ключ
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.created_at}')"
```

## Создание базы данных

После определения моделей нужно создать таблицы в базе данных:

```python
# В контексте приложения создаем все таблицы
with app.app_context():
    db.create_all()
```

Это создаст файл `site.db` (для SQLite) со всеми таблицами, которые мы определили.

## Основные операции с базой данных

### 1. Добавление записей (Create)

```python
# Создаем нового пользователя
new_user = User(username='john', email='john@example.com', password='secret')
db.session.add(new_user)  # Добавляем в сессию
db.session.commit()  # Сохраняем изменения в базе
```

### 2. Получение записей (Read)

```python
# Получить всех пользователей
all_users = User.query.all()

# Получить пользователя по ID
user = User.query.get(1)

# Фильтрация записей
john = User.query.filter_by(username='john').first()
users_with_j = User.query.filter(User.username.like('j%')).all()
```

### 3. Обновление записей (Update)

```python
user = User.query.get(1)
user.email = 'new_email@example.com'
db.session.commit()
```

### 4. Удаление записей (Delete)

```python
user = User.query.get(1)
db.session.delete(user)
db.session.commit()
```

## Пример CRUD приложения (Create, Read, Update, Delete)

### Главный файл приложения (app.py)

```python
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = 'secret-key-123'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель статьи
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}')"

# Создаем таблицы перед первым запросом
@app.before_first_request
def create_tables():
    db.create_all()

# Главная страница - список всех статей
@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

# Страница создания новой статьи
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        if not title or not content:
            flash('Заполните все поля!', 'danger')
        else:
            post = Post(title=title, content=content)
            db.session.add(post)
            db.session.commit()
            flash('Статья успешно создана!', 'success')
            return redirect(url_for('index'))
    
    return render_template('create.html')

# Страница редактирования статьи
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = Post.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        flash('Статья успешно обновлена!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit.html', post=post)

# Удаление статьи
@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Статья успешно удалена!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
```

### Шаблоны

#### templates/base.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>Flask Blog</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

#### templates/index.html

```html
{% extends "base.html" %}

{% block content %}
    <h1 class="mb-4">Все статьи</h1>
    <a href="{{ url_for('create') }}" class="btn btn-primary mb-3">Создать статью</a>
    
    {% if posts %}
        <div class="list-group">
            {% for post in posts %}
                <div class="list-group-item">
                    <div class="d-flex justify-content-between">
                        <h5>{{ post.title }}</h5>
                        <div>
                            <a href="{{ url_for('edit', id=post.id) }}" class="btn btn-sm btn-warning">Редактировать</a>
                            <a href="{{ url_for('delete', id=post.id) }}" class="btn btn-sm btn-danger" onclick="return confirm('Удалить статью?')">Удалить</a>
                        </div>
                    </div>
                    <p class="mb-1">{{ post.content[:100] }}{% if post.content|length > 100 %}...{% endif %}</p>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="alert alert-info">Статей пока нет</div>
    {% endif %}
{% endblock %}
```

#### templates/create.html

```html
{% extends "base.html" %}

{% block content %}
    <h1 class="mb-4">Создать статью</h1>
    <form method="POST">
        <div class="mb-3">
            <label for="title" class="form-label">Заголовок</label>
            <input type="text" class="form-control" id="title" name="title" required>
        </div>
        <div class="mb-3">
            <label for="content" class="form-label">Содержание</label>
            <textarea class="form-control" id="content" name="content" rows="5" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Создать</button>
        <a href="{{ url_for('index') }}" class="btn btn-secondary">Отмена</a>
    </form>
{% endblock %}
```

#### templates/edit.html

```html
{% extends "base.html" %}

{% block content %}
    <h1 class="mb-4">Редактировать статью</h1>
    <form method="POST">
        <div class="mb-3">
            <label for="title" class="form-label">Заголовок</label>
            <input type="text" class="form-control" id="title" name="title" value="{{ post.title }}" required>
        </div>
        <div class="mb-3">
            <label for="content" class="form-label">Содержание</label>
            <textarea class="form-control" id="content" name="content" rows="5" required>{{ post.content }}</textarea>
        </div>
        <button type="submit" class="btn btn-primary">Сохранить</button>
        <a href="{{ url_for('index') }}" class="btn btn-secondary">Отмена</a>
    </form>
{% endblock %}
```

## Связи между таблицами

### Один-ко-многим (One-to-Many)

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```

Использование:

```python
# Создание поста с автором
user = User.query.get(1)
post = Post(title='First Post', author=user)
db.session.add(post)
db.session.commit()

# Получение всех постов пользователя
user = User.query.get(1)
posts = user.posts  # Благодаря relationship

# Получение автора поста
post = Post.query.get(1)
author = post.author  # Благодаря backref
```

## Миграции базы данных

Для управления изменениями структуры базы данных используем Flask-Migrate:

```bash
pip install flask-migrate
```

Настройка:

```python
from flask_migrate import Migrate

app = Flask(__name__)
# ... остальная конфигурация ...
db = SQLAlchemy(app)
migrate = Migrate(app, db)
```

Использование:

```bash
# Инициализация (один раз)
flask db init

# Создание миграции (после изменения моделей)
flask db migrate -m "Описание изменений"

# Применение миграции
flask db upgrade
```

## Советы и лучшие практики

1. Всегда используйте `db.session.commit()` после изменений
2. Для выборки одной записи используйте `get()` или `first()`, а не `all()[0]`
3. Используйте `filter_by` для простых условий и `filter` для сложных
4. Для обработки ошибок используйте `get_or_404()` вместо `get()`
5. Закрывайте сессии в конце запроса (Flask-SQLAlchemy делает это автоматически)
6. Используйте миграции для изменения структуры базы данных

## Заключение

Flask-SQLAlchemy предоставляет удобный способ работы с базами данных в Flask-приложениях. Вы можете:
- Определять модели как Python-классы
- Выполнять CRUD-операции с простым синтаксисом
- Работать со связями между таблицами
- Управлять изменениями структуры базы через миграции

Это мощный инструмент, который значительно упрощает работу с базами данных в веб-приложениях.