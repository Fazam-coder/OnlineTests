from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField


class QuestionForm(FlaskForm):
    title = StringField('Введите вопрос')
    answer_a = StringField('а) (Обязательно)')
    answer_b = StringField('б)')
    answer_c = StringField('в)')
    answer_d = StringField('г)')
    correct_answer = RadioField('Пометьте верный вариант ответа', choices=[('1', 'а'),
                                ('2', 'б'), ('3', 'в'), ('4', 'г')], default='1')
    submit = SubmitField('Сохранить вопрос')
