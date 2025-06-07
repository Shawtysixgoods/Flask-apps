# Импорт необходимых модулей
from flask import Flask, render_template, redirect, url_for, flash, request, session

# Создание экземпляра приложения Flask
# __name__ указывает на текущий модуль (обычно имя файла)
app = Flask(__name__)

# Установка секретного ключа
# Требуется для работы сессий и flash-сообщений, которые используют криптографическую подпись
# В реальных проектах используйте длинную случайную строку и храните в безопасности
app.secret_key = 'supersecretkey'

# Базовый маршрут приложения
@app.route('/')
def index():
    """
    Главная страница приложения.
    Отображает все flash-сообщения и текущую сессию.
    """
    # Рендеринг шаблона index.html
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Страница входа с обработкой формы.
    Демонстрирует различные типы flash-сообщений.
    """
    if request.method == 'POST':
        # Получаем данные из формы
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Простая проверка учетных данных
        if not username or not password:
            # Flash с категорией 'error'
            flash('Все поля обязательны для заполнения!', 'error')
        elif username == 'admin' and password == 'secret':
            # Сохраняем пользователя в сессии
            session['user'] = username
            # Flash с категорией 'success'
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('index'))
        else:
            # Flash с категорией 'warning'
            flash('Неверные учетные данные!', 'warning')
    
    # Для GET-запросов или неверных данных POST показываем форму
    return render_template('login.html')

@app.route('/logout')
def logout():
    """
    Выход из системы с flash-сообщением.
    Удаляет пользователя из сессии.
    """
    if 'user' in session:
        # Получаем имя пользователя перед удалением
        username = session.pop('user')
        # Flash с дополнительными данными (необязательно)
        flash(f'Пользователь {username} вышел из системы.', 'info')
    return redirect(url_for('index'))

@app.route('/protected')
def protected():
    """
    Защищенная страница, доступная только авторизованным пользователям.
    Демонстрирует проверку доступа с flash-сообщением.
    """
    if 'user' not in session:
        flash('Доступ запрещен! Требуется авторизация.', 'danger')
        return redirect(url_for('login'))
    
    return render_template('protected.html', username=session['user'])

# Запуск приложения в режиме отладки (только для разработки)
if __name__ == '__main__':
    app.run(debug=True)