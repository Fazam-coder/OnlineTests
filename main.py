from flask import Flask, render_template
from flask_login import current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Fazam_secret_key'


@app.route('/')
def index():
    return render_template('base.html', title='Онлайн тесты', current_user=current_user)


@app.route('/register')
def register():
    pass


def main():
    app.run()


if __name__ == '__main__':
    main()
