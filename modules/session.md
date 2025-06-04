# Flask Sessions

Сессии в Flask - это механизм для хранения данных между запросами одного и того же пользователя. Это похоже на "корзину покупок" в интернет-магазине - информация сохраняется, пока пользователь взаимодействует с сайтом.

## Основные понятия

1. **Сессия** - временное хранилище данных на сервере
2. **Куки** - небольшие текстовые файлы, хранящиеся в браузере пользователя
3. **Ключ сессии** - уникальный идентификатор, связывающий пользователя с его данными

## Установка и базовая настройка

Для работы с сессиями в Flask не нужно устанавливать дополнительные пакеты - все уже включено:

```python
from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Обязательно для работы сессий
```

## Как работают сессии

1. Пользователь делает первый запрос к серверу
2. Сервер создает уникальный идентификатор сессии
3. Идентификатор отправляется в cookie браузера
4. При последующих запросах браузер отправляет идентификатор обратно
5. Сервер использует идентификатор для доступа к данным сессии

## Основные операции с сессиями

### 1. Запись данных в сессию

```python
@app.route('/login')
def login():
    # Записываем данные пользователя в сессию
    session['username'] = 'john_doe'
    session['logged_in'] = True
    session['user_id'] = 42
    return "Вы вошли в систему!"
```

### 2. Чтение данных из сессии

```python
@app.route('/profile')
def profile():
    # Проверяем, авторизован ли пользователь
    if not session.get('logged_in'):
        return "Пожалуйста, войдите в систему"
    
    # Получаем данные из сессии
    username = session['username']
    user_id = session['user_id']
    
    return f"""
        Профиль пользователя:
        Имя: {username}
        ID: {user_id}
    """
```

### 3. Удаление данных из сессии

```python
@app.route('/logout')
def logout():
    # Удаляем конкретные данные
    session.pop('username', None)
    session.pop('logged_in', None)
    
    # Или полностью очищаем сессию
    session.clear()
    
    return "Вы вышли из системы"
```

## Полный пример приложения с аутентификацией

```python
from flask import Flask, session, redirect, url_for, request, render_template, flash

app = Flask(__name__)
app.secret_key = 'super_secret_key_123'  # В реальном приложении используйте сложный ключ

# Моковая база пользователей (в реальном приложении используйте БД)
users = {
    'john': {'password': 'secret123', 'name': 'John Doe'},
    'alice': {'password': 'alice2023', 'name': 'Alice Smith'}
}

@app.route('/')
def home():
    # Проверяем, авторизован ли пользователь
    if 'username' in session:
        return render_template('home.html', 
                           username=session['username'],
                           name=users[session['username']]['name'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Проверяем учетные данные
        if username in users and users[username]['password'] == password:
            # Сохраняем в сессии факт входа
            session['username'] = username
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Удаляем данные пользователя из сессии
    session.pop('username', None)
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
```

## Шаблоны для примера

### templates/base.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>Flask Session Example</title>
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

### templates/login.html

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
        <button type="submit" class="btn btn-primary">Войти</button>
    </form>
{% endblock %}
```

### templates/home.html

```html
{% extends "base.html" %}

{% block content %}
    <h1>Добро пожаловать, {{ name }}!</h1>
    <p>Вы вошли как <strong>{{ username }}</strong></p>
    
    <div class="mt-4">
        <h3>Что вы можете сделать:</h3>
        <ul>
            <li>Посмотреть свой профиль</li>
            <li>Изменить настройки</li>
            <li>Выйти из системы</li>
        </ul>
    </div>
    
    <a href="{{ url_for('logout') }}" class="btn btn-danger mt-3">Выйти</a>
{% endblock %}
```

## Важные особенности сессий в Flask

1. **Хранение данных**: По умолчанию сессии хранятся в подписанных cookie браузера
2. **Размер данных**: Ограничены 4KB (из-за хранения в cookie)
3. **Безопасность**: Данные подписаны, но не зашифрованы (не храните пароли!)
4. **Время жизни**: По умолчанию - до закрытия браузера

## Как изменить параметры сессии

```python
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Сессия будет жить 7 дней (даже после закрытия браузера)
app.permanent_session_lifetime = timedelta(days=7)

@app.route('/login')
def login():
    session.permanent = True  # Применяем настройку времени жизни для этой сессии
    session['username'] = 'john'
    return "Вы вошли в систему"
```

## Альтернативные хранилища сессий

Для больших объемов данных или повышенной безопасности можно использовать серверные хранилища:

### 1. Redis

```python
from flask_session import Session

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = 'redis://localhost:6379'

Session(app)
```

### 2. База данных

```python
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db  # Ваш экземпляр SQLAlchemy
app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'  # Имя таблицы
```

## Безопасность сессий

1. **Секретный ключ**: Всегда используйте сложный `secret_key`
2. **HTTPS**: Для защиты от перехвата используйте HTTPS
3. **Чувствительные данные**: Не храните пароли и платежные данные в сессии
4. **Время жизни**: Устанавливайте разумное время жизни сессии

## Практические примеры использования

### Корзина покупок

```python
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    
    session['cart'].append(product_id)
    session.modified = True  # Явно указываем, что сессия изменена
    return "Товар добавлен в корзину"

@app.route('/cart')
def view_cart():
    cart_items = session.get('cart', [])
    return f"Товаров в корзине: {len(cart_items)}"
```

### Запоминание настроек пользователя

```python
@app.route('/set_theme/<theme>')
def set_theme(theme):
    if theme in ['light', 'dark']:
        session['theme'] = theme
        return f"Тема изменена на {theme}"
    return "Недопустимая тема"

# В шаблоне можно использовать:
# {% if session.get('theme') == 'dark' %} ... {% endif %}
```

## Отладка сессий

Для просмотра содержимого сессии:

```python
@app.route('/debug_session')
def debug_session():
    return dict(session)
```

## Частые ошибки и решения

1. **Сессия не сохраняется**: Убедитесь, что установлен `secret_key`
2. **Изменения не применяются**: Используйте `session.modified = True`
3. **Слишком большие данные**: Используйте серверное хранилище сессий
4. **Неожиданный выход**: Проверьте время жизни сессии

## Заключение

Сессии в Flask - это мощный инструмент для:
- Аутентификации пользователей
- Хранения временных данных
- Персонализации пользовательского опыта
- Реализации сложной логики взаимодействия

Запомните главные правила:
1. Всегда устанавливайте `secret_key`
2. Не храните конфиденциальные данные в cookie-сессиях
3. Используйте подходящее время жизни сессии
4. Для больших данных выбирайте серверное хранилище

