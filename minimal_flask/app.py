# Импортируем необходимые компоненты Flask
from flask import Flask, render_template, request, redirect, url_for

# Создаем приложение Flask - это основа нашего веб-сайта
app = Flask(__name__)

# Временное хранилище данных (в реальном приложении используется база данных)
items = []

@app.route('/')  # Декоратор указывает, какой URL будет вызывать эту функцию
def index():
    """Главная страница сайта"""
    # render_template рендерит HTML-файл, передавая в него данные
    return render_template(
        'index.html',
        title='Минимальный Flask',
        items=items
    )

@app.route('/about')
def about():
    """Страница "О проекте": демонстрация используемых технологий."""
    return render_template('about.html',
                           title='О проекте',
                           framework='Flask',
                           template_engine='Jinja2')

@app.route('/item/<string:name>')
def item(name):
    """Динамическая страница, которая получает параметр из URL.
       Демонстрирует, как передавать данные через маршруты.
    """
    return render_template('item.html',
                           title=f'Элемент {name}',
                           item_name=name)

@app.route('/add_item', methods=['POST'])
def add_item():
    """Обработчик формы добавления элемента.
       Извлекает данные из запроса и обновляет список.
    """
    new_item = request.form.get('item')
    if new_item:
        items.append(new_item)
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    """Пользовательская страница ошибки 404."""
    return render_template('404.html', title='Страница не найдена'), 404

if __name__ == '__main__':
    # Запуск приложения в режиме отладки (debug=True) включает автоперезагрузку и подробные сообщения об ошибках.
    app.run(debug=True)
