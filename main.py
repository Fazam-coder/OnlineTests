from flask import Flask, render_template, request
from flask_login import current_user, LoginManager, login_user, login_required, logout_user
from werkzeug.utils import redirect

from data import db_functions
from data.constants import *
from data.question import Question
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


def get_questions_in_test(test_id):
    questions = db_functions.select_questions_in_test(test_id)
    for i in range(len(questions)):
        quest = questions[i]
        questions[i] = Question(quest[QUESTION_TITLE], quest[ANSWER_A], quest[ANSWER_B],
                                quest[ANSWER_C], quest[ANSWER_D], quest[CORRECT_ANSWER],
                                quest[TEST_ID])
    return questions


@app.route('/')
def index():
    tests = db_functions.select_all_tests()
    for i in range(len(tests)):
        test = tests[i]
        tests[i] = Test(test[TEST_TITLE], test[USER_ID])
    tests = tests[::-1]
    return render_template('index.html', title='Онлайн тесты',
                           current_user=current_user, tests=tests)


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
    questions = get_questions_in_test(id)
    if form.validate_on_submit():
        if form.add_question.data:
            return redirect(f'/add_question/{id}')
        if form.submit.data:
            return redirect('/')
    return render_template('test.html', title='Создание теста', form=form, current_user=current_user,
                           preparation=False, questions=questions)


@app.route('/add_question/<int:test_id>', methods=['GET', 'POST'])
def add_question(test_id):
    form = QuestionForm()
    if form.validate_on_submit():
        if not form.title.data:
            return render_template('questions.html', title='Создание вопроса', form=form,
                                   current_user=current_user, message='Вопрос не введён')
        if not form.answer_a.data:
            return render_template('questions.html', title='Создание вопроса', form=form,
                                   current_user=current_user, message='Варианты ответов не введены')
        if ((form.correct_answer.data == 2 and not form.answer_b.data) or
            (form.correct_answer.data == 3 and not form.answer_c.data) or
            (form.correct_answer.data == 4 and not form.answer_d.data)):
            return render_template('questions.html', title='Создание вопроса', form=form,
                                   current_user=current_user, message='Верный вариант ответа не введён')
        question = Question(form.title.data, form.answer_a.data, form.answer_b.data,
                            form.answer_c.data, form.answer_d.data, form.correct_answer.data, test_id)
        if question.id:
            return render_template('questions.html', title='Создание вопроса', form=form,
                                   current_user=current_user, message='Такой вопрос уже существует')
        question.add()
        return redirect(f'/add_test/{test_id}')
    return render_template('question.html', title='Создание вопроса', form=form, current_user=current_user)


@app.route('/pass_test/<int:test_id>', methods=['GET', 'POST'])
def pass_test(test_id):
    test_info = db_functions.select_test(test_id)
    test = Test(test_info[TEST_TITLE], test_info[USER_ID])
    questions = get_questions_in_test(test_id)
    if request.form.get('submit'):
        answers = []
        count_correct_answers = 0
        for i in range(len(questions)):
            answer = request.form.get(str(i))
            if answer:
                answers.append(int(answer))
                if int(answer) == questions[i].correct_answer:
                    count_correct_answers += 1
            else:
                answers.append(None)
        return render_template('test_result.html', title='Результаты теста', test=test,
                               questions=questions, answers=answers, current_user=current_user,
                               count_correct_answers=count_correct_answers)
    return render_template('pass_test.html', title='Прохождение теста',
                           test=test, current_user=current_user, questions=questions)


def main():
    app.run()


if __name__ == '__main__':
    main()
