from flask import Flask, request, abort
from flask_restful import Resource, Api
from models import db, Post
from datetime import datetime

app = Flask(__name__)
# Настройка подключения к базе данных для API-приложения
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog_api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()  # Создаем таблицы, если не существуют

class PostListResource(Resource):
    def get(self):
        """Возвращает список всех статей в формате JSON."""
        posts = Post.query.order_by(Post.created.desc()).all()
        return [post.as_dict() for post in posts], 200

    def post(self):
        """Создает новую статью из данных JSON."""
        data = request.get_json()
        if not data or not data.get('title') or not data.get('content'):
            abort(400, "Title and content required")
        post = Post(
            title=data['title'],
            content=data['content'],
            created=datetime.utcnow()
        )
        db.session.add(post)
        db.session.commit()
        return post.as_dict(), 201

class PostResource(Resource):
    def get(self, post_id):
        """Возвращает конкретную статью по id."""
        post = Post.query.get_or_404(post_id)
        return post.as_dict(), 200

    def put(self, post_id):
        """Обновляет статью по id."""
        post = Post.query.get_or_404(post_id)
        data = request.get_json()
        if not data:
            abort(400, "No input data provided")
        post.title = data.get('title', post.title)
        post.content = data.get('content', post.content)
        db.session.commit()
        return post.as_dict(), 200

    def delete(self, post_id):
        """Удаляет статью по id."""
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return {"message": "Deleted"}, 204

api.add_resource(PostListResource, '/api/posts')
api.add_resource(PostResource, '/api/posts/<int:post_id>')

@app.route('/')
def index():
    # Простейшее приветственное сообщение для проверки работы API-приложения.
    return "Welcome to Blog API built on Flask", 200

if __name__ == '__main__':
    app.run(debug=True)
