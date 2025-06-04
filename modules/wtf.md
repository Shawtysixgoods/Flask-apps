### Flask-WTF 

Flask-WTF — это расширение для Flask, которое упрощает работу с веб-формами. Оно объединяет Flask с библиотекой WTForms, предоставляя удобные инструменты для создания форм, валидации данных и защиты от CSRF-атак. Давайте разберемся по шагам.

---

### 1. Установка
```bash
pip install Flask-WTF
```

---

### 2. Минимальный пример приложения
```python
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key_here"  # Обязательно для CSRF-защиты!

# Создаем класс формы (наследуемся от FlaskForm)
class LoginForm(FlaskForm):
    # Поля формы = КлассПоля(Метка, [валидаторы])
    username = StringField(
        "Имя пользователя", 
        validators=[
            DataRequired(message="Обязательное поле!"),  # Проверка на пустоту
            Length(min=3, max=20, message="Длина 3-20 символов")  # Проверка длины
        ]
    )
    password = PasswordField(
        "Пароль", 
        validators=[DataRequired()]
    )
    submit = SubmitField("Войти")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    
    # Если форма отправлена и прошла валидацию
    if form.validate_on_submit():
        # Обработка данных (здесь просто редирект)
        return redirect(url_for("success"))
    
    # Рендерим шаблон с формой (при GET или ошибках валидации)
    return render_template("login.html", form=form)

@app.route("/success")
def success():
    return "Успешный вход!"

if __name__ == "__main__":
    app.run(debug=True)
```

---

### 3. Разберем ключевые компоненты

#### 3.1 Класс формы (`FlaskForm`)
- **Наследование**: Все формы создаются как классы-наследники `FlaskForm`.
- **Поля**: Каждое поле — экземпляр класса (`StringField`, `PasswordField` и т.д.).
- **Валидаторы**:
  - `DataRequired()` — поле не может быть пустым.
  - `Length(min, max)` — ограничение длины.
  - `Email()` — проверка формата email.
  - `EqualTo("field")` — совпадение с другим полем (для паролей).
  - `Regexp(pattern)` — проверка по регулярному выражению.

#### 3.2 Контроллер (View-функция)
- `form = LoginForm()` — создаем экземпляр формы.
- `form.validate_on_submit()` — проверяет:
  - Был ли запрос `POST`?
  - Прошла ли валидация данных?
- При успехе — обрабатываем данные (например, сохраняем в БД).
- При ошибках — форма автоматически возвращается с сообщениями.

---

### 4. Шаблон `login.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>Вход</title>
</head>
<body>
    <h1>Форма входа</h1>
    
    <form method="POST">
        {{ form.hidden_tag() }}  <!-- CSRF-токен (обязательно!) -->
        
        <div>
            {{ form.username.label }}<br>
            {{ form.username(size=32) }}
            {% if form.username.errors %}
                <ul>
                    {% for error in form.username.errors %}
                        <li style="color: red;">{{ error }}</li>
                    {% endfor %}
                </ul>
            {% endif %}
        </div>
        
        <div>
            {{ form.password.label }}<br>
            {{ form.password(size=32) }}
            {% if form.password.errors %}
                <ul>
                    {% for error in form.password.errors %}
                        <li style="color: red;">{{ error }}</li>
                    {% endfor %}
                </ul>
            {% endif %}
        </div>
        
        {{ form.submit() }}
    </form>
</body>
</html>
```

#### Что здесь важно:
- `{{ form.hidden_tag() }}` — добавляет скрытое поле с CSRF-токеном (защита от подделки запросов).
- `{{ form.field.label }}` — метка поля.
- `{{ form.field() }}` — само поле ввода.
- Вывод ошибок: `form.field.errors` содержит список сообщений об ошибках.

---

### 5. Дополнительные возможности

#### 5.1 Кастомные валидаторы
```python
from wtforms.validators import ValidationError

def validate_custom(form, field):
    if "badword" in field.data.lower():
        raise ValidationError("Недопустимое слово в поле!")

class MyForm(FlaskForm):
    text = StringField("Текст", validators=[validate_custom])
```

#### 5.2 Загрузка файлов
```python
from flask_wtf.file import FileField, FileAllowed, FileRequired

class UploadForm(FlaskForm):
    photo = FileField(
        "Фото",
        validators=[
            FileRequired(),  # Файл обязателен
            FileAllowed(["jpg", "png"], "Только изображения!")  # Разрешенные типы
        ]
    )
    submit = SubmitField("Загрузить")
```

#### 5.3 Селекторы и чекбоксы
```python
from wtforms import SelectField, BooleanField

class SurveyForm(FlaskForm):
    age = SelectField(
        "Ваш возраст", 
        choices=[(18, "18-25"), (26, "26-35"), (36, "36+")]
    )
    agree = BooleanField("Согласен с условиями", validators=[DataRequired()])
```

---

### 6. Работа с данными формы
```python
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Доступ к данным формы:
        username = form.username.data
        password = form.password.data
        
        # Пример: Сохранение в БД
        user = User(username=username, password=hash(password))
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for("profile"))
    return render_template("register.html", form=form)
```

---

### 7. Важные нюансы
1. **SECRET_KEY**: Обязателен для работы CSRF-защиты. Должен быть сложным и секретным!
2. **Методы запроса**: Формы требуют указания `methods=["GET", "POST"]` в роуте.
3. **CSRF-защита**: Всегда используйте `{{ form.hidden_tag() }}` в шаблоне.
4. **Настройка полей**: Можно передавать HTML-атрибуты:
   ```python
   {{ form.username(class="input-field", placeholder="Ваше имя") }}
   ```

---

### 8. Что делать при ошибках?
- **Ошибки валидации**: Автоматически выводятся в шаблоне через `form.field.errors`.
- **Кастомные ошибки**: Используйте `flash()` для глобальных сообщений:
  ```python
  if user_exists(form.username.data):
      flash("Пользователь уже существует!", "error")
      return redirect(url_for("register"))
  ```

---

### Итог
Flask-WTF предоставляет:
- Простой ООП-подход к созданию форм
- Мощную валидацию данных
- Автоматическую CSRF-защиту
- Интеграцию с шаблонами Jinja2

