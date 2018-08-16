from passlib.hash import sha256_crypt
from mysql import get_connection


class User:

    @staticmethod
    def login(email_id, password):
        connection = get_connection()
        sql = "SELECT * FROM users WHERE email_id = '%s'" % email_id
        with connection.cursor() as cursor:
            cursor.execute(sql)
            if cursor.rowcount == 0:
                connection.close()
                return [False, 'Email Id']
            else:
                results = cursor.fetchone()
                if sha256_crypt.verify(password, results['password']):
                    connection.close()
                    return [True, results]
                else:
                    connection.close()
                    return [False, "Password"]

    @staticmethod
    def check_email_id(email_id):
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE email_id = '%s'" % email_id
            cursor.execute(sql)
            if cursor.rowcount == 0:
                connection.close()
                return False
            else:
                connection.close()
                return True

    @staticmethod
    def sign_up():
        pass
        # password = sha256_crypt.hash(str(123))
        # sql = "INSERT INTO users VALUES ('%s', '%s', '%s', '%s')" % ("sanjay@pfcmail.com", 'Sanjay Jain', password, '126')
        # cursor.execute(sql)
        # db.commit()


