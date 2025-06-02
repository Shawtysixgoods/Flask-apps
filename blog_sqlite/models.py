from flask_sqlalchemy import SQLAlchemy

# Создаем объект базы данных
db = SQLAlchemy()

class Post(db.Model):
    """Модель для хранения статей в блоге"""
    # Определяем структуру таблицы
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор
    title = db.Column(db.String(150), nullable=False)  # Заголовок статьи
    content = db.Column(db.Text, nullable=False)  # Текст статьи
    created = db.Column(db.DateTime, nullable=False)  # Дата создания
    
    def __repr__(self):
        """Строковое представление объекта для отладки"""
        return f'<Post {self.title}>'
