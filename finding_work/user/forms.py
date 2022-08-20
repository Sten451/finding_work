from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from finding_work.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Ник пользователя:',
                           validators=[DataRequired(),
                                       Length(min=2, max=20)])
    password = PasswordField('Пароль:', validators=[
                             DataRequired(), Length(min=5, max=30)])
    confirm_password = PasswordField('Подтвердить пароль',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    user_status = SelectField('Выбор статуса', choices=[
        ('CLIENT', 'Пользователь'), ('GUEST', 'Гость')])
    code = StringField('Код:',
                       validators=[DataRequired(),
                                   ])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Это имя занято. Пожалуйста, выберите другое.')


class LoginForm(FlaskForm):
    username = StringField('Ник пользователя:', validators=[DataRequired(), Length(
        min=2, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
