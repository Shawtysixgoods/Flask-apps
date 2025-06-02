from flask import Flask, render_template, request, redirect, url_for, abort
from models import db, Post, Comment, Tag
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog_comments_tags.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

class CommentForm(FlaskForm):
    """Форма для добавления комментария."""
    author = StringField('Автор', validators=[DataRequired()])
    content = TextAreaField('Комментарий', validators=[DataRequired()])
    submit = SubmitField('Отправить')

class NewPostForm(FlaskForm):
    """Форма для создания новой статьи с поддержкой тегов."""
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Контент', validators=[DataRequired()])
    tags = StringField('Тэги (через запятую)')
    submit = SubmitField('Создать запись')

@app.route('/')
def index():
    """Главная страница: вывод списка статей."""
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    """Страница статьи с комментариями и формой добавления нового комментария."""
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
        return redirect(url_for('post_detail', post_id=post.id))
    return render_template('post.html', post=post, form=form)

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    """Страница создания новой статьи с возможностью добавления тэгов."""
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            created=datetime.utcnow()
        )
        # Обработка тэгов, разделенных запятой
        tag_names = [t.strip() for t in form.tags.data.split(',') if t.strip()]
        for name in tag_names:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
                db.session.add(tag)
            post.tags.append(tag)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_post.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
