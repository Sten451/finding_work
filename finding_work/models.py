import enum
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
csrf = CSRFProtect()


class Status_Post(enum.Enum):
    NEW = "Новое"
    ANSWER = "Откликнулся"
    NOT_INTERESTING = "Не интересно(сложно)"
    REJECT = "Отказано"
    CLOSED = 'Объявление закрыто'


class Post(db.Model):
    """Модель вакансии"""
    id = db.Column(db.Integer, primary_key=True)
    id_hh = db.Column(db.Integer, nullable=False)
    href = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    salary = db.Column(db.String, nullable=False)
    experience = db.Column(db.String, nullable=False)
    type_of_work = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    note = db.Column(db.String, default=None)
    status = db.Column(db.Enum(Status_Post), default=Status_Post.NEW)
