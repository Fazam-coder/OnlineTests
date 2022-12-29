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
