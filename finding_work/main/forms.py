from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class NoteForm(FlaskForm):
    note = TextAreaField('Заметка', render_kw={
                         "placeholder": "........"}, validators=[DataRequired()])
    submit = SubmitField('СОХРАНИТЬ')


class StatusForm(FlaskForm):
    status = SelectField('Выбор статуса', choices=[
        ('NEW', 'Новое'), ('ANSWER', 'Откликнулся'), ('NOT_INTERESTING', 'Не интересно(сложно)'), ('REJECT', 'Отказано'), ('CLOSED', 'Объявление закрыто')])
    submit = SubmitField('ИЗМЕНИТЬ СТАТУС')
