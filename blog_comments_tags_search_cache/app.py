from flask import Flask, render_template, request, redirect, url_for, abort
from models import db, Post, Comment, Tag
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_caching import Cache

app = Flask(__name__)
# Настройка приложения: секретный ключ, база данных SQLite и параметры кеширования
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog_search_cache.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

db.init_app(app)
cache = Cache(app)

with app.app_context():
    db.create_all()

class CommentForm(FlaskForm):
    """Форма для добавления комментария."""
    author = StringField('Автор', validators=[DataRequired()])
    content = TextAreaField('Комментарий', validators=[DataRequired()])
    submit = SubmitField('Отправить')

class NewPostForm(FlaskForm):
    """Форма для создания новой статьи с тегами."""
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Контент', validators=[DataRequired()])
    tags = StringField('Тэги (через запятую)')
    submit = SubmitField('Создать запись')

@app.route('/')
@cache.cached()
def index():
    """Главная страница с кешированием, выводящая список статей."""
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    """Страница статьи с комментариями и формой для их добавления.
       GET-запросы могут кешироваться, POST приводит к сбросу кеша.
    """
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            post_id=post.id,
            author=form.author.data,
            content=form.content.data,
            created=datetime.utcnow()
        )
        db.session.add(comment)
        db.session.commit()
        cache.delete_memoized(index)
        return redirect(url_for('post_detail', post_id=post.id))
    return render_template('post.html', post=post, form=form)

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    """Страница создания новой статьи с добавлением тегов."""
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            created=datetime.utcnow()
        )
        # Обработка введенных тегов
        tag_names = [t.strip() for t in form.tags.data.split(',') if t.strip()]
        for name in tag_names:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
                db.session.add(tag)
            post.tags.append(tag)
        db.session.add(post)
        db.session.commit()
        cache.delete_memoized(index)
        return redirect(url_for('index'))
    return render_template('new_post.html', form=form)

@app.route('/search', methods=['GET'])
@cache.cached(query_string=True)
def search():
    """Страница поиска по статьям (по заголовку и содержимому)."""
    query = request.args.get('q', '')
    posts = []
    if query:
        posts = Post.query.filter(
            (Post.title.ilike(f'%{query}%')) | (Post.content.ilike(f'%{query}%'))
        ).order_by(Post.created.desc()).all()
    return render_template('search.html', posts=posts, query=query)

if __name__ == '__main__':
    app.run(debug=True)
