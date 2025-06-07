# Импортируем FlaskForm — базовый класс для всех форм Flask-WTF
from flask_wtf import FlaskForm

# Импортируем поля формы и валидаторы
from wtforms import StringField, SubmitField  # Поля для ввода текста и кнопка отправки
from wtforms.validators import DataRequired, Length  # Валидаторы для проверки данных

# Определяем форму с помощью Flask-WTF
class NameForm(FlaskForm):
    # Поле для ввода имени пользователя
    # StringField — поле для ввода строки
    # validators — список валидаторов, которые будут применяться к этому полю
    # DataRequired — проверяет, что поле не пустое
    # Length — проверяет длину строки
    # Подробнее: https://wtforms.readthedocs.io/en/3.0.x/fields/#wtforms.fields.StringField
    name = StringField(
        'Введите ваше имя',  # Метка для поля (отображается в шаблоне)
        validators=[
            DataRequired(message="Поле обязательно для заполнения"),
            Length(min=2, max=20, message="Имя должно быть от 2 до 20 символов")
        ]
    )
    # Кнопка отправки формы
    submit = SubmitField('Отправить')
