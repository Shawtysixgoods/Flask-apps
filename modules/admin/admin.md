### Flask-Admin

Flask-Admin — это расширение Flask для быстрого создания административных интерфейсов. Оно позволяет управлять данными вашего приложения через веб-интерфейс без написания большого количества кода. Разберем всё по шагам.

---

### 1. Установка
```bash
pip install flask-admin
```

---

### 2. Минимальный пример с SQLAlchemy

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Инициализация SQLAlchemy
db = SQLAlchemy(app)

# Создаем простую модель
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# Создаем экземпляр Flask-Admin
admin = Admin(app, name='My Admin Panel', template_mode='bootstrap3')

# Добавляем представление для модели
admin.add_view(ModelView(User, db.session))

# Создаем таблицы в базе данных
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
```

После запуска перейдите по адресу `http://localhost:5000/admin`.

---

### 3. Разберем ключевые компоненты

#### 3.1 Модель данных (User)
- Обычная SQLAlchemy модель
- Определяет структуру данных (таблицу в БД)

#### 3.2 ModelView
- Класс, который создает интерфейс для работы с моделью
- Автоматически генерирует:
  - Список записей
  - Формы создания/редактирования
  - Кнопки удаления
  - Пагинацию
  - Поиск и фильтрацию

#### 3.3 Admin
- Основной класс Flask-Admin
- `template_mode`: стиль интерфейса (bootstrap3 или bootstrap4)

---

### 4. Кастомизация представлений

Создаем кастомный класс представления:

```python
class CustomUserView(ModelView):
    # Какие столбцы отображать в списке
    column_list = ['id', 'username', 'email']
    
    # Поля для поиска
    column_searchable_list = ['username', 'email']
    
    # Фильтры
    column_filters = ['username']
    
    # Редактируемые поля в списке (без перехода в форму)
    column_editable_list = ['username']
    
    # Форматирование столбцов
    column_labels = dict(username='Логин', email='E-mail')
    
    # Форма создания/редактирования
    form_columns = ['username', 'email']
    
    # Настройки пагинации
    page_size = 20
    
    # Запрет на создание новых записей
    can_create = True
    
    # Запрет на удаление
    can_delete = True
    
    # Экспорт данных
    can_export = True

# Регистрируем кастомное представление
admin.add_view(CustomUserView(User, db.session, name='Пользователи'))
```

---

### 5. Работа с отношениями между моделями

Добавим модель постов с отношением к пользователю:

```python
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))

# Кастомное представление для постов
class PostView(ModelView):
    # Отображаем пользователя через отношение
    column_list = ['title', 'user', 'content']
    
    # Форма создания поста с выбором пользователя
    form_columns = ['title', 'content', 'user']
    
    # AJAX-подгрузка пользователей (для больших таблиц)
    form_ajax_refs = {
        'user': {
            'fields': ['username', 'email'],
            'page_size': 10
        }
    }

admin.add_view(PostView(Post, db.session, name='Посты'))
```

---

### 6. Аутентификация и авторизация

Защитим админ-панель с помощью Flask-Login:

```python
from flask_login import LoginManager, UserMixin, current_user

# Настройка Flask-Login
login_manager = LoginManager(app)

# Обновляем модель пользователя
class User(UserMixin, db.Model):
    # ... (поля из предыдущего примера)
    is_admin = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Создаем защищенное представление
class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        # Перенаправляем на страницу входа, если нет доступа
        return redirect(url_for('login'))

# Используем защищенное представление
admin.add_view(SecureModelView(User, db.session))
admin.add_view(SecureModelView(Post, db.session))
```

---

### 7. Кастомные действия

Добавим действие для массового обновления записей:

```python
class PostView(SecureModelView):
    # ... предыдущие настройки ...
    
    # Добавляем кастомное действие
    @action('approve', 'Одобрить', 'Вы уверены, что хотите одобрить выбранные записи?')
    def action_approve(self, ids):
        try:
            # Получаем выбранные записи
            posts = Post.query.filter(Post.id.in_(ids))
            
            # Обновляем записи
            for post in posts:
                post.approved = True
                
            db.session.commit()
            flash(f'{len(ids)} постов одобрено', 'success')
        except Exception as e:
            flash(f'Ошибка: {str(e)}', 'error')

# Добавляем в список действий
PostView.actions = ['approve']
```

---

### 8. Кастомные страницы

Создадим свою страницу в админ-панели:

```python
from flask_admin import BaseView, expose

class AnalyticsView(BaseView):
    @expose('/')
    def index(self):
        # Логика для сбора статистики
        user_count = User.query.count()
        post_count = Post.query.count()
        return self.render('admin/analytics.html', 
                          user_count=user_count,
                          post_count=post_count)

# Добавляем кастомную страницу
admin.add_view(AnalyticsView(name='Аналитика', endpoint='analytics'))
```

Создайте шаблон `templates/admin/analytics.html`:
```html
{% extends 'admin/master.html' %}
{% block body %}
  <h1>Статистика</h1>
  <p>Пользователей: {{ user_count }}</p>
  <p>Постов: {{ post_count }}</p>
{% endblock %}
```

---

### 9. Важные настройки

```python
# Глобальная конфигурация Flask-Admin
admin = Admin(
    app,
    name='My Admin',
    template_mode='bootstrap4',
    index_view=CustomHomeView()
)

# Кастомная домашняя страница
class CustomHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return super().index()
```

---

### 10. Расширенные возможности

#### Экспорт данных
```python
class UserView(ModelView):
    can_export = True
    export_types = ['csv', 'xlsx']
    column_export_list = ['id', 'username']  # Какие столбцы экспортировать
```

#### WYSIWYG-редактор
```python
from flask_admin.contrib.sqla.form import AdminModelConverter
from wtforms import TextAreaField
from flask_ckeditor import CKEditorField

class PostView(ModelView):
    form_overrides = dict(content=CKEditorField)
    create_template = 'admin/ckeditor.html'
    edit_template = 'admin/ckeditor.html'
```

#### Переопределение шаблонов
Создайте в своей папке templates:
```
/templates
    /admin
        /model
            list.html  # Шаблон списка записей
            create.html # Шаблон создания
            edit.html   # Шаблон редактирования
```

---

### 11. Полный пример приложения

```python
from flask import Flask, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'supersecretkey'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# Модель пользователя
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy=True)

# Модель поста
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Защищенное представление
class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

# Кастомная домашняя страница
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return super().index()

# Инициализация Flask-Admin
admin = Admin(
    app, 
    name='Админ-панель', 
    template_mode='bootstrap4',
    index_view=MyAdminIndexView()
)

# Регистрация представлений
admin.add_view(SecureModelView(User, db.session, name='Пользователи'))
admin.add_view(SecureModelView(Post, db.session, name='Посты'))

# Маршруты для аутентификации
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Упрощенная реализация для примера
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    
    # В реальном приложении проверяйте логин/пароль!
    user = User.query.filter_by(is_admin=True).first()
    if user:
        login_user(user)
        return redirect(url_for('admin.index'))
    
    return "Нет администратора в базе!"

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Создание таблиц
@app.before_first_request
def create_tables():
    db.create_all()
    # Создаем тестового администратора
    if not User.query.first():
        admin_user = User(
            username='admin',
            email='admin@example.com',
            password='adminpassword',  # В реальности хешируйте пароли!
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
```

---

### 12. Советы для новичков

1. **Начните с простого**: Сначала используйте базовый ModelView, затем добавляйте кастомизацию
2. **Безопасность**:
   - Всегда защищайте админ-панель
   - Никогда не храните пароли в открытом виде
   - Ограничивайте доступ по ролям
3. **Постепенное усложнение**:
   - Сначала работайте с простыми моделями
   - Затем добавляйте отношения между моделями
   - Потом внедряйте кастомные представления
4. **Используйте миграции**: Для управления изменениями БД используйте Flask-Migrate
5. **Документация**: Изучайте официальную документацию Flask-Admin

