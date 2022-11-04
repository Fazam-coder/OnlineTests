import sqlite3
from .constants import *

con = sqlite3.connect(DB_NAME)
cur = con.cursor()


def edit_user(*args):
    pass


def delete_user(id):
    query = f''
    cur.execute(query)
    con.commit()