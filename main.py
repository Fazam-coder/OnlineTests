from flask import Flask, render_template
from flask_login import current_user, LoginManager, login_user, login_required, logout_user
from werkzeug.utils import redirect

from data import db_functions
from data.constants import *
from data.test import Test
from forms.login import LoginForm
from forms.question import QuestionForm
from forms.register import RegisterForm

from data.user import User, check_user_password
from forms.test import TestForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Fazam_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user_info = db_functions.select_user(user_id)
    return User(user_info[NAME], user_info[EMAIL], user_info[PASSWORD], user_info[ABOUT])


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def index():
    return render_template('index.html', title='Онлайн тесты', current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', message='Пароли не совпадают',
                                   title='Регистрация', form=form, current_user=current_user)
        user = User(form.name.data, form.email.data, form.password.data, form.about.data)
        if user.id:
            return render_template('register.html', message='Такой пользователь уже есть',
                                   title='Регистрация', form=form, current_user=current_user)
        user.add()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        id = db_functions.get_user_id(form.name.data, form.email.data)
        if not id:
            return render_template('login.html', message='Такого пользователя нет',
                                   title='Авторизация', form=form, current_user=current_user)
        user_info = db_functions.select_user(id)
        password = user_info[PASSWORD]
        if check_user_password(password, form.password.data):
            user = User(user_info[NAME], user_info[EMAIL], form.password.data, user_info[ABOUT])
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message='Неверный пароль',
                               title='Авторизация', form=form, current_user=current_user)
    return render_template('login.html', title='Авторизация', form=form, current_user=current_user)


# Создание теста без вопросов, вопросы добавлять, переходя на страницу редактирования теста
# В HTML отличать создание от редактирования с помощью bool
# Уменьшить кол-во кнопок и условий к ним
@app.route('/add_test', methods=['GET', 'POST'])
def add_test_start():
    form = TestForm()
    if form.validate_on_submit():
        if not form.title.data:
            return render_template('test.html', message='Тест не назван',
                                   title='Создание теста', form=form, current_user=current_user,
                                   preparation=True)
        test = Test(form.title.data, current_user.id)
        if not test.id:
            test.add()
            return redirect(f'/add_test/{test.id}')
        else:
            return render_template('test.html', message='Такой тест уже существует',
                                   title='Создание теста', form=form, current_user=current_user,
                                   preparation=True)
    return render_template('test.html', title='Создание теста', form=form, current_user=current_user,
                           preparation=True)


@app.route('/add_test/<int:id>', methods=['GET', 'POST'])
def add_test_end(id):
    form = TestForm()
    test_info = db_functions.select_test(id)
    form.title.data = test_info[TEST_TITLE]
    return render_template('test.html', title='Создание теста', form=form, current_user=current_user,
                           preparation=False)


@app.route('/add_question/<int:test_id>', methods=['GET', 'POST'])
def add_question(test_id):
    form = QuestionForm()
    return render_template('question.html', title='Создание вопроса', form=form, current_user=current_user)


def main():
    app.run()


if __name__ == '__main__':
    main()
