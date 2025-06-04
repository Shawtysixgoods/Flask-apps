from flask import Flask, render_template, abort
import markdown
import frontmatter
import os
from datetime import datetime

app = Flask(__name__)

# Абсолютный путь к каталогу с Markdown-файлами (статьями)
CONTENT_DIR = os.path.join(os.path.dirname(__file__), 'content')

def get_posts():
    """Извлекает и сортирует статьи из каталога CONTENT_DIR по дате."""
    posts = []
    for filename in os.listdir(CONTENT_DIR):
        if filename.endswith('.md'):
            with open(os.path.join(CONTENT_DIR, filename), 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                # Создаем slug статьи из имени файла (без расширения)
                post.metadata['slug'] = filename[:-3]
                # Преобразуем строку с датой в объект datetime
                if isinstance(post.metadata.get('date'), str):
                    post.metadata['date'] = datetime.strptime(post.metadata['date'], '%Y-%m-%d')
                posts.append(post)
    return sorted(posts, key=lambda post: post.metadata.get('date', datetime.min), reverse=True)

def get_post(slug):
    """Возвращает конкретную статью по slug или None, если файл не найден."""
    filepath = os.path.join(CONTENT_DIR, f'{slug}.md')
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
        # Преобразуем Markdown в HTML с помощью библиотеки markdown
        post.content = markdown.markdown(post.content)
        return post

@app.route('/')
def index():
    """Главная страница: вывод списка статей из Markdown-файлов."""
    posts = get_posts()
    return render_template('index.html', posts=posts)

@app.route('/post/<slug>')
def post(slug):
    """Страница отображения одной статьи по slug."""
    post_obj = get_post(slug)
    if post_obj is None:
        abort(404)
    return render_template('post.html', post=post_obj)

if __name__ == '__main__':
    # Запуск приложения с режимом отладки
    app.run(debug=True)
