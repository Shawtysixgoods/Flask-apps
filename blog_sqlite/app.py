from flask import Flask, render_template, request, redirect, url_for, abort
from models import db, Post
from datetime import datetime

app = Flask(__name__)
# Настройка подключения к базе SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()  # Создание таблиц при первом запуске

@app.route('/')
def index():
    """Главная страница, отображающая список статей, отсортированных по дате."""
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    """Страница подробного просмотра статьи по её идентификатору."""
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    """Страница создания новой статьи.
       При POST-запросе данные формы сохраняются в базе.
    """
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if not title or not content:
            abort(400, "Title and Content required")
        post = Post(title=title, content=content, created=datetime.utcnow())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_post.html')

if __name__ == '__main__':
    # Запуск приложения в режиме отладки (debug=True)
    app.run(debug=True)
