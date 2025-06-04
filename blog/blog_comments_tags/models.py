from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Ассоциативная таблица для связи многих ко многим между Post и Tag
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Post(db.Model):
    """Модель статьи блога."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    # Связь с комментариями (один ко многим)
    comments = db.relationship('Comment', backref='post', cascade="all, delete-orphan", lazy=True)
    # Связь с тегами (многие ко многим)
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy=True))

class Comment(db.Model):
    """Модель комментария к статье."""
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False)

class Tag(db.Model):
    """Модель тэга для статьи."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
