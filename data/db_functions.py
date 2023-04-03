import sqlite3
from .constants import *

con = sqlite3.connect(DB_NAME, check_same_thread=False)
cur = con.cursor()


def get_user_id(name, email):
    query = f"""SELECT {ID} FROM {USERS}
                WHERE {NAME} = '{name}' AND {EMAIL} = '{email}'"""
    user_id = cur.execute(query).fetchall()
    if user_id:
        return user_id[0][0]
    return None


def select_user(id):
    query = f"""SELECT * FROM {USERS} WHERE {ID} = {id}"""
    result = cur.execute(query).fetchone()
    user_info = {ID: result[0], NAME: result[1], EMAIL: result[2],
                 PASSWORD: result[3], ABOUT: result[4], CREATED_DATE: result[5]}
    return user_info


def edit_user(id, name, login, password, about):
    query = f"""UPDATE {USERS} 
                SET {NAME} = '{name}', {EMAIL} = '{login}', 
                {PASSWORD} = '{password}', {ABOUT} = '{about}'
                WHERE {ID} = {id}"""
    cur.execute(query)
    con.commit()


def delete_user(id):
    query = f'DELETE FROM {USERS} WHERE {ID} = {id}'
    cur.execute(query)
    con.commit()


def get_test_id(title, user_id):
    query = f"""SELECT {ID} FROM {TESTS} 
                WHERE {TEST_TITLE} = '{title}' AND {USER_ID} = '{user_id}'"""
    test_id = cur.execute(query).fetchall()
    if test_id:
        return test_id[0][0]
    return None


def select_test(id):
    query = f"""SELECT * FROM {TESTS} WHERE {ID} = {id}"""
    result = cur.execute(query).fetchone()
    test_info = {ID: result[0], TEST_TITLE: result[1], USER_ID: result[2]}
    return test_info


def get_question_id(title, a, b, c, d, correct, test_id):
    query = f"""SELECT {ID} FROM {QUESTIONS}
                WHERE {QUESTION_TITLE} = '{title}' AND {ANSWER_A} = '{a}' AND
                      {ANSWER_B} = '{b}' AND {ANSWER_C} = '{c}' AND {ANSWER_D} = '{d}' AND
                      {CORRECT_ANSWER} = '{correct}' AND {TEST_ID} = '{test_id}'"""
    question_id = cur.execute(query).fetchall()
    if question_id:
        return question_id[0][0]
    return None


def select_questions_in_test(test_id):
    query = f"""SELECT * FROM {QUESTIONS} WHERE {TEST_ID} = {test_id}"""
    questions = cur.execute(query).fetchall()
    result = []
    for question in questions:
        result.append({ID: question[0], QUESTION_TITLE: question[1], ANSWER_A: question[2],
                       ANSWER_B: question[3], ANSWER_C: question[4], ANSWER_D: question[5],
                       CORRECT_ANSWER: question[6], TEST_ID: question[7]})
    return result


def select_all_tests():
    query = f"""SELECT * FROM {TESTS}"""
    tests = cur.execute(query).fetchall()
    result = []
    for test in tests:
        result.append({ID: test[0], TEST_TITLE: test[1], USER_ID: test[2]})
    return result


def delete_test(id):
    query = f'DELETE FROM {TESTS} WHERE {ID} = {id}'
    cur.execute(query)
    con.commit()