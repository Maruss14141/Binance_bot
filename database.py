import sqlite3


connection = sqlite3.connect("bot_database.sqlite3", check_same_thread=False)


connection.execute('CREATE TABLE if not exists users(id integer, api_key text, secret_key text)')

# add user to database

def add_user(uid, api_key, secret_key):
    connection.execute("INSERT INTO users(id, api_key, secret_key) VALUES (?, ?, ?)", [uid, api_key, secret_key])
    connection.commit()




# get user by id

def get_user(uid):
    result = connection.execute("SELECT * FROM users WHERE id = ?", [uid]).fetchone()
    return result