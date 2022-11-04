from flask_login import UserMixin
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from .constants import *
from . import db_functions

con = sqlite3.connect(DB_NAME)

cur = con.cursor()


class User(UserMixin):
    def __init__(self, name, login, password, about):
        self.name = name
        self.login = login
        self.about = about
        self.created_date = '/'.join(str(datetime.date.today()).split('-')[::-1])
        self.set_password(password)
        self.id = self.get_id()

    def get_id(self):
        query = f"""SELECT {ID} FROM {USERS}
                    WHERE {NAME} = {self.name} AND {LOGIN} = {self.login}
                    AND {ABOUT} = {ABOUT} AND {PASSWORD} = {self.hashed_password}"""
        user_id = cur.execute(query).fetchone()
        return user_id[0] if len(user_id) == 1 else None

    def add(self):
        query = f"""INSERT INTO {USERS}({NAME}, {LOGIN}, {PASSWORD}, {ABOUT}, {CREATED_DATE}) 
                    VALUES({self.name}, {self.login}, {self.hashed_password}, {self.about}, {self.created_date})"""
        cur.execute(query)
        con.commit()
        self.id = self.get_id()

    def edit_name(self, name):
        self.name = name
        self.edit()

    def edit_login(self, login):
        self.login = login
        self.edit()

    def edit_password(self, password):
        self.set_password(password)
        self.edit()

    def edit_about(self, about):
        self.about = about
        self.edit()

    def edit(self):
        db_functions.edit_user(self.id, self.name, self.login, self.hashed_password, self.about)

    def delete(self):
        db_functions.delete_user(self.id)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
