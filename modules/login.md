# Flask-Login
Flask-Login - это расширение для Flask, которое упрощает реализацию аутентификации пользователей. Оно предоставляет готовые решения для:
- Управления сессиями пользователей
- Защиты маршрутов
- Работы с текущим пользователем
- Обработки "запомнить меня"

## Основные понятия

1. **Аутентификация** - процесс проверки подлинности пользователя
2. **Авторизация** - предоставление прав доступа
3. **User Session** - сессия авторизованного пользователя
4. **User Loader** - функция для загрузки пользователя из БД

## Установка

```bash
pip install flask flask-login flask-sqlalchemy
```

## Базовая настройка

### Инициализация приложения

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Инициализация Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Маршрут для входа
```

### Модель пользователя

```python
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    # Метод для представления объекта
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
```

### User Loader - загрузчик пользователя

```python
@login_manager.user_loader
def load_user(user_id):
    # Эта функция вызывается Flask-Login для получения объекта пользователя по ID
    return User.query.get(int(user_id))
```

## Основные функции Flask-Login

### 1. Вход пользователя (`login_user`)

```python
from flask import render_template, redirect, url_for, flash, request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # Проверка, авторизован ли уже пользователь
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Поиск пользователя в базе данных
        user = User.query.filter_by(username=username).first()
        
        # Проверка пароля (в реальном приложении используйте хеширование!)
        if user and user.password == password:
            # Авторизация пользователя
            login_user(user, remember=request.form.get('remember'))
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
    
    return render_template('login.html')
```

### 2. Выход пользователя (`logout_user`)

```python
@app.route('/logout')
@login_required  # Только для авторизованных пользователей
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('login'))
```

### 3. Защита маршрутов (`@login_required`)

```python
@app.route('/profile')
@login_required  # Требует авторизации
def profile():
    # current_user доступен во всех шаблонах и вьюшках после авторизации
    return render_template('profile.html', user=current_user)
```

### 4. Проверка состояния пользователя

```python
# В шаблоне или вьюшке:
if current_user.is_authenticated:
    # Пользователь авторизован
    print(f"Привет, {current_user.username}!")
else:
    # Пользователь не авторизован
    print("Пожалуйста, войдите в систему")
```

## Полный пример приложения

### app.py

```python
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Модель пользователя
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# Загрузчик пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Создаем базу данных
@app.before_first_request
def create_tables():
    db.create_all()
    
    # Создаем тестового пользователя, если его нет
    if not User.query.filter_by(username='admin').first():
        user = User(username='admin', email='admin@example.com', password='admin')
        db.session.add(user)
        db.session.commit()

# Главная страница
@app.route('/')
def home():
    return render_template('home.html')

# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember') == 'on'
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            login_user(user, remember=remember)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
    
    return render_template('login.html')

# Выход
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('home'))

# Профиль пользователя
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# Защищенная страница
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

if __name__ == '__main__':
    app.run(debug=True)
```

### Шаблоны

#### templates/base.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>Flask-Login Example</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('home') }}">Flask-Login</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    {% if current_user.is_authenticated %}
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('profile') }}">Профиль</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('dashboard') }}">Панель управления</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('logout') }}">Выйти</a>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('login') }}">Войти</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

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

#### templates/home.html

```html
{% extends "base.html" %}

{% block content %}
    <h1>Добро пожаловать!</h1>
    <p class="lead">Это пример приложения с аутентификацией на Flask-Login.</p>
    
    {% if current_user.is_authenticated %}
        <div class="alert alert-success">
            Вы вошли как: <strong>{{ current_user.username }}</strong>
        </div>
        <a href="{{ url_for('profile') }}" class="btn btn-primary">Ваш профиль</a>
        <a href="{{ url_for('dashboard') }}" class="btn btn-success">Панель управления</a>
    {% else %}
        <p>Пожалуйста, войдите в систему, чтобы получить доступ к дополнительным функциям.</p>
        <a href="{{ url_for('login') }}" class="btn btn-primary">Войти</a>
    {% endif %}
{% endblock %}
```

#### templates/login.html

```html
{% extends "base.html" %}

{% block content %}
    <h1 class="mb-4">Вход в систему</h1>
    <form method="POST" action="{{ url_for('login') }}">
        <div class="mb-3">
            <label for="username" class="form-label">Имя пользователя</label>
            <input type="text" class="form-control" id="username" name="username" required>
        </div>
        <div class="mb-3">
            <label for="password" class="form-label">Пароль</label>
            <input type="password" class="form-control" id="password" name="password" required>
        </div>
        <div class="mb-3 form-check">
            <input type="checkbox" class="form-check-input" id="remember" name="remember">
            <label class="form-check-label" for="remember">Запомнить меня</label>
        </div>
        <button type="submit" class="btn btn-primary">Войти</button>
    </form>
{% endblock %}
```

#### templates/profile.html

```html
{% extends "base.html" %}

{% block content %}
    <h1>Ваш профиль</h1>
    <div class="card mt-4">
        <div class="card-body">
            <h5 class="card-title">{{ user.username }}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{{ user.email }}</h6>
            <p class="card-text">ID пользователя: {{ user.id }}</p>
            <p class="card-text">Статус: 
                {% if user.is_authenticated %}
                    <span class="badge bg-success">Авторизован</span>
                {% else %}
                    <span class="badge bg-danger">Не авторизован</span>
                {% endif %}
            </p>
        </div>
    </div>
    
    <div class="mt-4">
        <h3>Действия:</h3>
        <a href="{{ url_for('dashboard') }}" class="btn btn-primary">Панель управления</a>
        <a href="{{ url_for('logout') }}" class="btn btn-danger">Выйти</a>
    </div>
{% endblock %}
```

#### templates/dashboard.html

```html
{% extends "base.html" %}

{% block content %}
    <h1>Панель управления</h1>
    <div class="alert alert-info mt-4">
        <strong>Только для авторизованных пользователей!</strong>
        <p>Это защищенная страница, которую видят только вошедшие в систему пользователи.</p>
    </div>
    
    <div class="card mt-4">
        <div class="card-header">
            Информация о пользователе
        </div>
        <div class="card-body">
            <h5 class="card-title">{{ user.username }}</h5>
            <p class="card-text">Email: {{ user.email }}</p>
            <p class="card-text">ID: {{ user.id }}</p>
        </div>
    </div>
    
    <div class="mt-4">
        <h3>Статистика:</h3>
        <ul class="list-group">
            <li class="list-group-item">Последний вход: Сегодня</li>
            <li class="list-group-item">Количество посещений: 5</li>
            <li class="list-group-item">Статус: Активен</li>
        </ul>
    </div>
{% endblock %}
```

## Расширенные возможности Flask-Login

### 1. Пользовательские анонимные пользователи

```python
from flask_login import AnonymousUserMixin

class MyAnonymousUser(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Гость'
        self.role = 'guest'

login_manager.anonymous_user = MyAnonymousUser
```

### 2. Обработка неавторизованных запросов

```python
@login_manager.unauthorized_handler
def unauthorized():
    flash('Для доступа к этой странице необходимо войти в систему', 'warning')
    return redirect(url_for('login'))
```

### 3. Работа с ролями пользователей

Добавьте в модель пользователя поле роли:

```python
class User(db.Model, UserMixin):
    # ... существующие поля ...
    role = db.Column(db.String(20), default='user')
    
    def has_role(self, role_name):
        return self.role == role_name
```

Использование:

```python
@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.has_role('admin'):
        flash('У вас недостаточно прав', 'danger')
        return redirect(url_for('home'))
    
    return render_template('admin.html')
```

### 4. "Запомнить меня" (Remember Me)

Flask-Login автоматически поддерживает функцию "запомнить меня". Для настройки времени жизни сессии:

```python
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)  # 30 дней
```

## Безопасность

1. **Хеширование паролей** - никогда не храните пароли в открытом виде!
    ```python
    from werkzeug.security import generate_password_hash, check_password_hash

    # При создании пользователя
    user = User(username='admin', password=generate_password_hash('admin'))

    # При проверке пароля
    if check_password_hash(user.password, password):
        # Пароль верный
    ```

2. **Защита от CSRF** - используйте Flask-WTF для форм
3. **HTTPS** - всегда используйте при работе с аутентификацией
4. **Сложный секретный ключ**

## Лучшие практики

1. Всегда используйте `@login_required` для защищенных маршрутов
2. Регулярно обновляйте зависимости
3. Используйте сложные пароли и хеширование
4. Ограничивайте попытки входа
5. Реализуйте восстановление пароля

## Заключение

Flask-Login предоставляет мощные инструменты для:
- Управления пользовательскими сессиями
- Защиты маршрутов
- Работы с текущим пользователем
- Реализации функции "запомнить меня"

Основные компоненты:
1. `UserMixin` - добавляет необходимые методы в модель пользователя
2. `user_loader` - загружает пользователя из БД
3. `login_user()` - авторизует пользователя
4. `logout_user()` - завершает сеанс
5. `current_user` - доступ к текущему пользователю
6. `@login_required` - защита маршрутов

