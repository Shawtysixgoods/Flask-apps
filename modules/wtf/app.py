# Импортируем необходимые модули из стандартной библиотеки Python и Flask
# Flask — основной класс для создания приложения
from flask import Flask, render_template, redirect, url_for, flash
# FlaskForm — базовый класс для всех форм Flask-WTF
from flask_wtf import FlaskForm
# Импортируем поля формы из WTForms
from wtforms import StringField, SubmitField
# Импортируем валидаторы для проверки данных формы
from wtforms.validators import DataRequired

# Создаём экземпляр Flask-приложения
# __name__ — имя текущего модуля, нужно для корректной работы Flask
app = Flask(__name__)
# Устанавливаем секретный ключ, необходимый для защиты от CSRF-атак и работы flash-сообщений
# Подробнее: https://flask.palletsprojects.com/en/latest/config/#SECRET_KEY
app.config['SECRET_KEY'] = 'очень_секретный_ключ'

# Определяем форму с помощью FlaskForm
# Подробнее: https://flask-wtf.readthedocs.io/en/stable/
class NameForm(FlaskForm):
    # StringField — поле для ввода текста
    # label — подпись к полю
    # validators — список валидаторов, например, DataRequired требует обязательного заполнения
    name = StringField('Введите ваше имя', validators=[DataRequired()])
    # SubmitField — кнопка отправки формы
    submit = SubmitField('Отправить')

# Главная страница, поддерживает методы GET и POST
@app.route('/', methods=['GET', 'POST'])
def index():
    # Создаём экземпляр формы
    form = NameForm()
    # Проверяем, была ли отправлена форма и прошла ли она валидацию
    if form.validate_on_submit():
        # Получаем значение поля name
        name = form.name.data
        # flash — функция для отображения временных сообщений пользователю
        # Подробнее: https://flask.palletsprojects.com/en/latest/patterns/flashing/
        flash(f'Привет, {name}!')
        # После POST-запроса делаем редирект на главную страницу (Post/Redirect/Get паттерн)
        return redirect(url_for('index'))
    # Рендерим шаблон index.html и передаём в него форму
    return render_template('index.html', form=form)

# Запуск приложения только если файл запущен напрямую
if __name__ == '__main__':
    # app.run() запускает встроенный сервер Flask
    # debug=True включает режим отладки (не использовать в продакшене)
    app.run(debug=True)
