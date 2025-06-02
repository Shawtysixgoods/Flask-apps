from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Post(db.Model):
    """Модель статьи для блога, используемая в API."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def as_dict(self):
        """Метод для преобразования данных модели в словарь."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created': self.created.isoformat()
        }
