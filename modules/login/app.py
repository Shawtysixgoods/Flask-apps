# Импортируем необходимые модули из стандартной библиотеки Python и Flask
# Flask — основной класс для создания приложения
from flask import Flask, render_template, redirect, url_for, request, flash
# Импортируем flask_login для управления сессиями пользователей
# Подробнее: https://flask-login.readthedocs.io/en/latest/
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Создаём экземпляр Flask-приложения
app = Flask(__name__)
# Устанавливаем секретный ключ, необходимый для работы сессий и защиты от подделки cookie
app.config['SECRET_KEY'] = 'очень_секретный_ключ'

# Создаём экземпляр LoginManager — менеджер для управления логином пользователей
login_manager = LoginManager()
# Инициализируем LoginManager с нашим приложением
login_manager.init_app(app)
# Указываем, куда перенаправлять пользователя, если он не авторизован
login_manager.login_view = 'login'  # имя функции (view), а не url

# Для примера создаём простую структуру пользователей (обычно используется база данных)
# Ключ — имя пользователя, значение — словарь с паролем
users = {
    'admin': {'password': 'adminpass'},
    'user': {'password': 'userpass'}
}

# Класс пользователя должен наследовать UserMixin для совместимости с Flask-Login
class User(UserMixin):
    # Конструктор принимает имя пользователя
    def __init__(self, username):
        self.id = username  # id — обязательное поле для Flask-Login

    # Метод для получения пользователя по id (обязателен для Flask-Login)
    @staticmethod
    def get(user_id):
        # Проверяем, есть ли пользователь в нашей структуре
        if user_id in users:
            return User(user_id)
        return None

# Функция-коллбек для загрузки пользователя по id из сессии
# Подробнее: https://flask-login.readthedocs.io/en/latest/#how-it-works
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Главная страница
@app.route('/')
@login_required  # Декоратор требует авторизации для доступа к странице
def index():
    # current_user — специальный объект Flask-Login, содержит текущего пользователя
    return render_template('index.html', username=current_user.id)

# Страница логина, поддерживает методы GET и POST
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Если запрос POST, значит пользователь отправил форму
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Проверяем, есть ли пользователь и совпадает ли пароль
        if username in users and users[username]['password'] == password:
            user = User(username)
            # login_user — функция для входа пользователя (создаёт сессию)
            login_user(user)
            flash('Вы успешно вошли!')
            # После входа перенаправляем на главную страницу
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль')
    # Если GET-запрос или ошибка, отображаем форму логина
    return render_template('login.html')

# Страница выхода
@app.route('/logout')
@login_required  # Только для авторизованных пользователей
def logout():
    # logout_user — функция для выхода пользователя (удаляет сессию)
    logout_user()
    flash('Вы вышли из системы')
    return redirect(url_for('login'))

# Запуск приложения только если файл запущен напрямую
if __name__ == '__main__':
    # app.run() запускает встроенный сервер Flask
    # debug=True включает режим отладки (не использовать в продакшене)
    app.run(debug=True)
