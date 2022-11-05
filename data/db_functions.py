import sqlite3
from .constants import *

con = sqlite3.connect(DB_NAME)
cur = con.cursor()


def select_user(id):
    query = f"""SELECT * FROM {USERS} WHERE {ID} = {id}"""
    result = cur.execute(query).fetchone()
    user_info = {ID: result[0], NAME: result[1], EMAIL: result[2],
                 PASSWORD: result[3], ABOUT: result[4], CREATED_DATE: result[5]}
    return user_info


def edit_user(id, name, login, password, about):
    query = f"""UPDATE {USERS} 
                SET {NAME} = {name}, {EMAIL} = {login}, 
                {PASSWORD} = {password}, {ABOUT} = {about}
                WHERE {ID} = {id}"""
    cur.execute(query)
    con.commit()


def delete_user(id):
    query = f'DELETE FROM {USERS} WHERE {ID} = {id}'
    cur.execute(query)
    con.commit()
