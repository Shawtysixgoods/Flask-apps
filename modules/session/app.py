# Импортируем необходимые модули из стандартной библиотеки Python и Flask
# Flask — основной класс для создания приложения
from flask import Flask, session, redirect, url_for, request, render_template

# Создаём экземпляр Flask-приложения
# __name__ — имя текущего модуля, нужно для корректной работы Flask
app = Flask(__name__)
# Устанавливаем секретный ключ, необходимый для работы сессий и защиты от подделки cookie
# Подробнее: https://flask.palletsprojects.com/en/latest/config/#SECRET_KEY
app.config['SECRET_KEY'] = 'очень_секретный_ключ'

# Главная страница, поддерживает методы GET и POST
@app.route('/', methods=['GET', 'POST'])
def index():
    # Если запрос POST, значит пользователь отправил форму
    if request.method == 'POST':
        # Получаем имя пользователя из формы
        username = request.form.get('username')
        # Сохраняем имя пользователя в сессии
        # session — специальный объект Flask, реализующий хранение данных между запросами
        # Подробнее: https://flask.palletsprojects.com/en/latest/quickstart/#sessions
        session['username'] = username
        # После POST-запроса делаем редирект на главную страницу (Post/Redirect/Get паттерн)
        return redirect(url_for('index'))
    # Получаем имя пользователя из сессии, если оно есть
    username = session.get('username')
    # Рендерим шаблон index.html и передаём в него имя пользователя
    return render_template('index.html', username=username)

# Маршрут для выхода пользователя (очистка сессии)
@app.route('/logout')
def logout():
    # Удаляем имя пользователя из сессии, если оно есть
    session.pop('username', None)
    # После выхода делаем редирект на главную страницу
    return redirect(url_for('index'))

# Запуск приложения только если файл запущен напрямую
if __name__ == '__main__':
    # app.run() запускает встроенный сервер Flask
    # debug=True включает режим отладки (не использовать в продакшене)
    app.run(debug=True)
