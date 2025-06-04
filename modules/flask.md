### Flask

Flask - это микрофреймворк для создания веб-приложений на Python. Он прост в изучении и дает полный контроль над приложением. Давайте разберем все основы шаг за шагом.

---

### 1. Установка
```bash
pip install flask
```

---

### 2. Минимальное приложение
```python
from flask import Flask

# Создаем экземпляр приложения Flask
# __name__ нужно для определения местоположения ресурсов
app = Flask(__name__)

# Декоратор route связывает URL с функцией
@app.route('/')
def home():
    # Возвращаем простой текст
    return "Привет, мир!"

# Запускаем сервер, если файл выполняется напрямую
if __name__ == '__main__':
    # debug=True включает режим отладки (только для разработки!)
    app.run(debug=True)
```

После запуска перейдите по адресу `http://localhost:5000`.

---

### 3. Основные компоненты Flask

#### 3.1 Роутинг (маршрутизация)
```python
@app.route('/about')
def about():
    return "О нас"

# Маршрут с переменной частью
@app.route('/user/<username>')
def show_user(username):
    return f'Пользователь: {username}'

# Можно указывать тип переменной
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Пост #{post_id}'

# Несколько URL для одной функции
@app.route('/home')
@app.route('/index')
@app.route('/main')
def index():
    return "Главная страница"
```

#### 3.2 HTTP-методы
```python
# По умолчанию разрешен только GET
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Обработка данных формы
        return "Вы вошли!"
    else:
        # Показать форму входа
        return '''
            <form method="POST">
                <input type="text" name="username">
                <input type="password" name="password">
                <input type="submit" value="Войти">
            </form>
        '''
```

---

### 4. Работа с запросами (request)
```python
from flask import request

@app.route('/search')
def search():
    # Получаем параметры из URL: /search?q=query
    query = request.args.get('q', '')  # Второй аргумент - значение по умолчанию
    return f'Результаты поиска: {query}'

@app.route('/submit', methods=['POST'])
def submit():
    # Данные формы
    username = request.form['username']
    password = request.form.get('password', '')
    
    # Загружаем файл
    file = request.files['file']
    if file:
        file.save('uploads/' + file.filename)
    
    return "Данные получены!"
```

---

### 5. Шаблоны (Jinja2)
Flask использует шаблонизатор Jinja2 для HTML.

#### Структура проекта:
```
myapp/
├── app.py
├── templates/
│   ├── base.html
│   ├── home.html
│   └── user.html
└── static/
    ├── style.css
    └── script.js
```

#### base.html (базовый шаблон)
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <header>
        <h1>Мой сайт</h1>
    </header>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        &copy; 2023
    </footer>
</body>
</html>
```

#### home.html (наследуем от базового)
```html
{% extends "base.html" %}

{% block title %}Главная страница{% endblock %}

{% block content %}
    <h2>Добро пожаловать!</h2>
    <p>Сегодня: {{ current_date }}</p>
    <ul>
        {% for item in items %}
            <li>{{ item }}</li>
        {% endfor %}
    </ul>
{% endblock %}
```

#### Рендеринг шаблона в роуте
```python
from flask import render_template
from datetime import datetime

@app.route('/')
def home():
    return render_template(
        'home.html',
        current_date=datetime.now().strftime("%d.%m.%Y"),
        items=['Яблоки', 'Бананы', 'Апельсины']
    )
```

---

### 6. Работа с ответами (response)
```python
from flask import make_response, redirect, url_for

@app.route('/custom')
def custom_response():
    # Создаем кастомный ответ
    response = make_response("Кастомный ответ")
    response.headers['X-Custom-Header'] = 'Значение'
    response.set_cookie('test_cookie', '12345')
    return response

@app.route('/old-url')
def old_url():
    # Перенаправление
    return redirect(url_for('home'))

@app.route('/json')
def json_example():
    # Возвращаем JSON
    from flask import jsonify
    return jsonify({'name': 'Alice', 'age': 30, 'city': 'Moscow'})

@app.route('/error')
def force_error():
    # Возвращаем статус ошибки
    return "Страница не найдена", 404
```

---

### 7. Сессии и куки
```python
from flask import session

# Секретный ключ нужен для подписи сессионных кук
app.secret_key = 'your_secret_key_here'

@app.route('/set-session')
def set_session():
    # Устанавливаем значение в сессии
    session['username'] = 'Alice'
    return "Сессия установлена"

@app.route('/get-session')
def get_session():
    # Получаем значение из сессии
    username = session.get('username', 'Гость')
    return f"Привет, {username}!"

@app.route('/logout')
def logout():
    # Удаляем значение из сессии
    session.pop('username', None)
    return "Вы вышли"
```

---

### 8. Обработка ошибок
```python
# Обработка 404 ошибки
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# Обработка 500 ошибки
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Пример генерации ошибки
@app.route('/divide/<int:a>/<int:b>')
def divide(a, b):
    try:
        result = a / b
        return str(result)
    except ZeroDivisionError:
        # Можно возвращать кастомную страницу
        return "Деление на ноль запрещено!", 400
```

---

### 9. Контекст приложения и запроса

#### Контекст приложения:
```python
# Доступ к конфигурации
app.config['DEBUG'] = True

# Регистрация функций для использования в шаблонах
@app.context_processor
def inject_user():
    def is_admin(user):
        return user == 'admin'
    return dict(is_admin=is_admin)  # Теперь is_admin доступна во всех шаблонах
```

#### Контекст запроса:
```python
from flask import g

@app.before_request
def before_request():
    # Выполняется перед каждым запросом
    g.start_time = time.time()
    g.user = get_current_user()  # Примерная функция

@app.teardown_request
def teardown_request(exception=None):
    # Выполняется после каждого запроса
    duration = time.time() - g.start_time
    print(f"Запрос выполнился за {duration:.2f} секунд")
```

---

### 10. Полный пример приложения
```python
from flask import Flask, render_template, request, session, redirect, url_for, g
import time
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Генерация случайного секретного ключа

# Простая "база данных" пользователей
USERS = {
    'alice': 'password123',
    'bob': 'qwerty'
}

@app.before_request
def load_user():
    g.user = None
    if 'username' in session:
        g.user = session['username']

@app.route('/')
def home():
    return render_template('home.html', user=g.user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Неверные данные!", 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/protected')
def protected():
    if not g.user:
        return redirect(url_for('login'))
    return f"Секретная страница для {g.user}"

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
```

#### templates/login.html:
```html
{% extends "base.html" %}

{% block content %}
<h2>Вход</h2>
<form method="POST">
    <label>Имя пользователя:
        <input type="text" name="username" required>
    </label>
    <label>Пароль:
        <input type="password" name="password" required>
    </label>
    <button type="submit">Войти</button>
</form>
{% endblock %}
```

