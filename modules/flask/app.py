# Импортируем класс Flask из пакета flask
# Flask — основной класс для создания веб-приложения
# Документация: https://flask.palletsprojects.com/en/latest/
from flask import Flask, render_template, request, redirect, url_for

# Создаём экземпляр приложения Flask
# __name__ — имя текущего модуля, используется для поиска ресурсов (шаблонов, статических файлов)
app = Flask(__name__)

# Определяем маршрут (URL), который будет обрабатывать функция
# @app.route('/') — декоратор, связывающий URL '/' с функцией index
# Подробнее: https://flask.palletsprojects.com/en/latest/quickstart/#routing
@app.route('/')
def index():
    # Функция возвращает результат, который будет отправлен пользователю
    # Обычно это HTML-страница, сгенерированная с помощью шаблона
    # render_template — функция для рендеринга HTML-шаблонов (Jinja2)
    # Подробнее: https://flask.palletsprojects.com/en/latest/quickstart/#rendering-templates
    return render_template('index.html')

# Пример маршрута с переменной в URL
# <name> — переменная часть URL, передаётся как аргумент функции
@app.route('/hello/<name>')
def hello(name):
    # Передаём переменную name в шаблон для отображения
    return render_template('hello.html', name=name)

# Пример маршрута, поддерживающего методы GET и POST
@app.route('/form', methods=['GET', 'POST'])
def form_example():
    # Если запрос POST, обрабатываем отправку формы
    if request.method == 'POST':
        # Получаем значение поля 'username' из формы
        username = request.form.get('username')
        # После обработки формы можно сделать редирект на другую страницу
        return redirect(url_for('hello', name=username))
    # Если GET-запрос — отображаем форму
    return render_template('form.html')

# Запуск приложения только если файл запущен напрямую
if __name__ == '__main__':
    # app.run() запускает встроенный сервер Flask
    # debug=True включает режим отладки (автоматический перезапуск при изменениях, подробные ошибки)
    # Не использовать debug=True в продакшене!
    app.run(debug=True)
