from flask import Flask
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Fazam_secret_key'


def main():
    db_session.global_init('db/tests.db')
    app.run()


if __name__ == '__main__':
    main()