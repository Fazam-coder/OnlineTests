from flask_login import UserMixin
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):
    def __init__(self):
        self.created_date = '/'.join(str(datetime.date.today()).split('-')[::-1])

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
