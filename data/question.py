from .constants import *
from data import db_functions

import sqlite3

con = sqlite3.connect(DB_NAME, check_same_thread=False)
cur = con.cursor()


class Question:
    def __init__(self, title, a, b, c, d, correct, test_id):
        self.title = title
        self.answer_a = a
        self.answer_b = b
        self.answer_c = c
        self.answer_d = d
        self.correct_answer = correct
        self.test_id = test_id
        self.id = self.get_id()

    def get_id(self):
        return db_functions.get_question_id(self.title, self.answer_a, self.answer_b,
                                            self.answer_c, self.answer_d, self.correct_answer,
                                            self.test_id)

    def add(self):
        if self.id:
            return
        query = f"""INSERT INTO {QUESTIONS}({QUESTION_TITLE}, {ANSWER_A}, {ANSWER_B}, 
                                            {ANSWER_C}, {ANSWER_D}, {CORRECT_ANSWER}, {TEST_ID})
                    VALUES ('{self.title}', '{self.answer_a}', '{self.answer_b}', 
                            '{self.answer_c}', '{self.answer_d}', '{self.correct_answer}', 
                            '{self.test_id}')"""
        cur.execute(query)
        con.commit()
        self.id = self.get_id()
