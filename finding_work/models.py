import enum
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_login import UserMixin


db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
bcrypt = Bcrypt()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Status_Post(enum.Enum):
    NEW = "Новое"
    ANSWER = "Откликнулся"
    NOT_INTERESTING = "Не интересно(сложно)"
    REJECT = "Отказано"
    CLOSED = 'Объявление закрыто'


class User(db.Model, UserMixin):
    """Модель юзера"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    user_status = db.Column(db.String, nullable=False)


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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Enum(Status_Post), default=Status_Post.NEW)
