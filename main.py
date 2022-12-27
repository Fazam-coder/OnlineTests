from flask import Flask, render_template
from flask_login import current_user
from werkzeug.utils import redirect

from forms.register import RegisterForm

from data.user import User
from data.constants import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Fazam_secret_key'


@app.route('/')
def index():
    return render_template('base.html', title='Онлайн тесты', current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', message='Пароли не совпадают',
                                   title='Регистрация', form=form, current_user=current_user)
        user = User(form.name.data, form.email.data, form.password.data, form.about.data)
        if user.get_id():
            return render_template('register.html', message='Такой пользователь уже есть',
                                   title='Регистрация', form=form, current_user=current_user)
        user.add()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return 'True'


def main():
    app.run()


if __name__ == '__main__':
    main()
