import sqlite3,os

DATABASE = 'homework.db'

def init_db():
    with open('homework.sql', encoding = "UTF-8") as f:
        create_db_sql = f.read()
        db = sqlite3.connect(DATABASE)
        db.executescript(create_db_sql)
        db.commit()

def remove_db():
    if os.path.isfile(DATABASE):
        os.remove(DATABASE) 

# 先刪除db,再create db ,sql內建一些資料
remove_db()
init_db()