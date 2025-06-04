from flask import Flask, render_template  # Импорт Flask и render_template для работы с HTML-шаблонами
from flask_admin import Admin  # Импорт Flask-Admin для создания админ-панели
from flask_admin.contrib.sqla import ModelView  # Импорт готовых представлений для моделей SQLAlchemy
from models import db, Post  # Импорт базы данных и модели Post

app = Flask(__name__)
# Настройка приложения: SECRET_KEY для защиты, параметры подключения к базе SQLite
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog_admin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()  # Создание таблиц в базе данных

# Инициализация админ-панели с использованием шаблона bootstrap3
admin = Admin(app, name='Blog Admin', template_mode='bootstrap3')
# Добавляем представление модели Post в админ-панель, чтобы администраторы могли управлять статьями
admin.add_view(ModelView(Post, db.session))

@app.route('/')
def index():
    """Публичная страница, показывающая список статей блога."""
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)
