from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class TestForm(FlaskForm):
    title = StringField('Введите название теста')
    add_question = SubmitField('Добавить вопрос')
    submit = SubmitField('Создать тест')