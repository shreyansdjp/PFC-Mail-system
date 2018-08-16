import pymysql

host = ''
username = ''
password = ''
db_name = ''


def get_connection():
    global host, username, password, db_name
    db = pymysql.connect(host, username, password, db_name, cursorclass=pymysql.cursors.DictCursor)
    return db

