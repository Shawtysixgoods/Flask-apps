from flask import Flask, render_template, request, redirect, url_for, abort
from models import db, Post, Comment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
# Настройка секретного ключа и параметров подключения к базе данных SQLite
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog_comments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()  # Создаем таблицы в базе, если еще не созданы

class CommentForm(FlaskForm):
    """Форма для добавления комментария к статье."""
    author = StringField('Автор', validators=[DataRequired()])
    content = TextAreaField('Комментарий', validators=[DataRequired()])
    submit = SubmitField('Отправить')

@app.route('/')
def index():
    """Главная страница: вывод списка статей."""
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    """Страница статьи с выводом комментариев и формой для их добавления."""
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        # Обработка отправки комментария
        comment = Comment(
            post_id=post.id,
            author=form.author.data,
            content=form.content.data,
            created=datetime.utcnow()
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('post_detail', post_id=post.id))
    return render_template('post.html', post=post, form=form)

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    """Страница создания новой статьи."""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if not title or not content:
            abort(400, "Title and content required.")
        post = Post(title=title, content=content, created=datetime.utcnow())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_post.html')

if __name__ == '__main__':
    app.run(debug=True)
