# Импортируем необходимые функции и классы из Flask
from flask import Blueprint, render_template, flash

# Импортируем форму, определённую в forms.py
from .forms import NameForm

# Создаём blueprint для группировки маршрутов, связанных с Flask-WTF
# Подробнее: https://flask.palletsprojects.com/en/latest/blueprints/
wtf_bp = Blueprint('wtf_demo', __name__)

# Главная страница с формой
@wtf_bp.route('/', methods=['GET', 'POST'])
def index():
    # Создаём экземпляр формы
    # Flask-WTF автоматически обрабатывает CSRF-токен и валидацию
    form = NameForm()
    # Проверяем, была ли отправлена форма и прошла ли она валидацию
    # form.validate_on_submit() возвращает True только если метод POST и все валидаторы прошли успешно
    # Подробнее: https://flask-wtf.readthedocs.io/en/stable/form.html#flask_wtf.FlaskForm.validate_on_submit
    if form.validate_on_submit():
        # Получаем значение поля name из формы
        name = form.name.data
        # flash — функция Flask для отправки временных сообщений пользователю
        flash(f'Привет, {name}!')
        # После обработки формы можно очистить поле (опционально)
        form.name.data = ''
    # Если GET-запрос или форма не прошла валидацию — просто отображаем страницу с формой
    return render_template('index.html', form=form)
