from flask_login import UserMixin
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from .constants import *
from . import db_functions

con = sqlite3.connect(DB_NAME, check_same_thread=False)

cur = con.cursor()


class User(UserMixin):
    def __init__(self, name, email, password, about):
        self.name = name
        self.email = email
        self.about = about
        self.created_date = '.'.join(str(datetime.date.today()).split('-')[::-1])
        self.id = db_functions.get_user_id(name, email)
        self.set_password(password)

    def add(self):
        if self.id:
            return
        query = f"""INSERT INTO {USERS}({NAME}, {EMAIL}, {PASSWORD}, {ABOUT}, {CREATED_DATE}) 
                    VALUES('{self.name}', '{self.email}', '{self.hashed_password}', '{self.about}', '{self.created_date}')"""
        cur.execute(query)
        con.commit()
        self.id = db_functions.get_user_id(self.name, self.email)

    def edit_name(self, name):
        self.name = name
        self.edit()

    def edit_login(self, login):
        self.email = login
        self.edit()

    def edit_password(self, password):
        self.set_password(password)
        self.edit()

    def edit_about(self, about):
        self.about = about
        self.edit()

    def edit(self):
        db_functions.edit_user(self.id, self.name, self.email, self.hashed_password, self.about)

    def delete(self):
        db_functions.delete_user(self.id)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)


def check_user_password(hashed_password, password):
    return check_password_hash(hashed_password, password)
