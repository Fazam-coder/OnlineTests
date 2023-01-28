import sqlite3

from data import db_functions
from data.constants import *

con = sqlite3.connect(DB_NAME, check_same_thread=False)
cur = con.cursor()


class Test:
    def __init__(self, title, user_id):
        self.title = title
        self.user_id = user_id
        self.id = self.get_id()
        self.user_name = self.get_user_name()

    def add(self):
        if self.id:
            return
        query = f"""INSERT INTO {TESTS}({TEST_TITLE}, {USER_ID})
                    VALUES ('{self.title}', '{self.user_id}')"""
        cur.execute(query)
        con.commit()
        self.id = self.get_id()

    def get_id(self):
        return db_functions.get_test_id(self.title, self.user_id)

    def get_user_name(self):
        return db_functions.select_user(self.user_id)[NAME]