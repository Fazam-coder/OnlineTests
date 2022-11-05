from flask import Flask, render_template
from flask_login import current_user

from forms.register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Fazam_secret_key'


@app.route('/')
def index():
    return render_template('base.html', title='Онлайн тесты', current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template('register.html', title='Регистрация', form=form, current_user=current_user)


def main():
    app.run()


if __name__ == '__main__':
    main()
