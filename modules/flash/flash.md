# Flask Flash - система сообщений для пользователя

Flask Flash - это механизм для передачи одноразовых сообщений между запросами в веб-приложении. Это особенно полезно, когда вам нужно показать пользователю сообщение об успешном выполнении действия или об ошибке после перенаправления на другую страницу.

## Основные понятия

1. **Flash сообщения** - это сообщения, которые хранятся в сессии пользователя только до следующего запроса.
2. **Сессия** - временное хранилище данных на сервере, связанное с конкретным пользователем.
3. **Шаблоны** - HTML-файлы с возможностью вставки Python-кода (используется Jinja2).

## Установка Flask

Прежде чем начать, убедитесь, что у вас установлен Flask:

```bash
pip install flask
```

## Базовый пример

```python
# Импортируем необходимые модули из Flask
from flask import Flask, flash, redirect, render_template, request, session, url_for

# Создаем экземпляр Flask приложения
app = Flask(__name__)

# Секретный ключ необходим для работы сессий (в реальном проекте используйте сложный ключ)
app.secret_key = 'super_secret_key_123'

# Главная страница
@app.route('/')
def index():
    # Просто рендерим шаблон index.html
    return render_template('index.html')

# Страница для входа (логина)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Получаем данные из формы
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Простая проверка (в реальном приложении используйте базу данных)
        if username == 'admin' and password == 'secret':
            # Если все правильно - создаем flash-сообщение об успехе
            flash('Вы успешно вошли в систему!', 'success')
            # Перенаправляем на главную страницу
            return redirect(url_for('index'))
        else:
            # Если ошибка - создаем flash-сообщение об ошибке
            flash('Неверное имя пользователя или пароль', 'error')
    
    # Рендерим шаблон login.html (и для GET запроса, и если POST запрос с ошибкой)
    return render_template('login.html')

# Запускаем приложение в режиме отладки
if __name__ == '__main__':
    app.run(debug=True)
```

## Шаблоны (HTML с Jinja2)

### templates/base.html (базовый шаблон)

```html
<!DOCTYPE html>
<html>
<head>
    <title>Мое Flask приложение</title>
    <!-- Подключаем Bootstrap для красоты (не обязательно) -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <!-- Блок для отображения flash сообщений -->
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
        
        <!-- Основное содержимое страницы -->
        {% block content %}{% endblock %}
    </div>
    
    <!-- Скрипты Bootstrap -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### templates/index.html (наследуется от base.html)

```html
{% extends "base.html" %}

{% block content %}
    <h1>Добро пожаловать на главную страницу!</h1>
    <p>Это пример использования Flask Flash сообщений.</p>
    <a href="{{ url_for('login') }}" class="btn btn-primary">Войти</a>
{% endblock %}
```

### templates/login.html (наследуется от base.html)

```html
{% extends "base.html" %}

{% block content %}
    <h1>Вход в систему</h1>
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

## Как это работает - пошагово

1. Пользователь заходит на страницу входа (`/login`) через GET запрос.
2. Вводит данные и отправляет форму (POST запрос).
3. Сервер проверяет данные:
   - Если верные: создает flash-сообщение с категорией 'success' и перенаправляет на главную страницу.
   - Если неверные: создает flash-сообщение с категорией 'error' и снова показывает форму входа.
4. При перенаправлении или обновлении страницы flash-сообщение извлекается из сессии и показывается пользователю.
5. После показа сообщение удаляется из сессии и больше не будет показываться.

## Дополнительные возможности

### Категории сообщений

Вы можете использовать разные категории для разных типов сообщений:

```python
flash('Сообщение об успехе', 'success')
flash('Предупреждение', 'warning')
flash('Ошибка', 'danger')
flash('Информация', 'info')
```

В шаблоне вы можете по-разному стилизовать сообщения в зависимости от категории.

### Фильтрация сообщений по категориям

```html
{% for category, message in get_flashed_messages(with_categories=true) %}
    {% if category == 'error' %}
        <div class="alert alert-danger">{{ message }}</div>
    {% elif category == 'success' %}
        <div class="alert alert-success">{{ message }}</div>
    {% else %}
        <div class="alert alert-info">{{ message }}</div>
    {% endif %}
{% endfor %}
```

### Несколько сообщений одновременно

Вы можете отправить несколько flash-сообщений подряд:

```python
flash('Первое сообщение', 'info')
flash('Второе сообщение', 'warning')
```

Они все будут показаны на следующей странице в том порядке, в котором были добавлены.

## Важные моменты

1. **Секретный ключ**: Для работы flash-сообщений (и сессий) необходимо установить `app.secret_key`.
2. **Перенаправления**: Flash работает лучше всего при использовании с `redirect()`, так как сообщения сохраняются между запросами.
3. **Одноразовость**: Сообщения удаляются после первого же их отображения.
4. **Шаблоны**: Для отображения сообщений нужно использовать `get_flashed_messages()` в шаблоне.

## Пример с формой обратной связи

Добавим еще один пример - форму обратной связи:

```python
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        if not all([name, email, message]):
            flash('Пожалуйста, заполните все поля', 'error')
        else:
            # Здесь мог бы быть код для отправки email или сохранения в БД
            flash('Ваше сообщение отправлено! Мы скоро свяжемся с вами.', 'success')
            return redirect(url_for('contact'))
    
    return render_template('contact.html')
```

Шаблон `templates/contact.html`:

```html
{% extends "base.html" %}

{% block content %}
    <h1>Обратная связь</h1>
    <form method="POST">
        <div class="mb-3">
            <label for="name" class="form-label">Ваше имя</label>
            <input type="text" class="form-control" id="name" name="name" required>
        </div>
        <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input type="email" class="form-control" id="email" name="email" required>
        </div>
        <div class="mb-3">
            <label for="message" class="form-label">Сообщение</label>
            <textarea class="form-control" id="message" name="message" rows="5" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Отправить</button>
    </form>
{% endblock %}
```

## Заключение

Flask Flash - это простой, но мощный механизм для передачи информации пользователю между запросами. Он особенно полезен при работе с формами и перенаправлениями. 

Основные шаги:
1. Используйте `flash()` во view-функциях для создания сообщений.
2. Используйте `get_flashed_messages()` в шаблонах для отображения сообщений.
3. Не забывайте про `app.secret_key`.
4. Используйте категории для разных типов сообщений.
