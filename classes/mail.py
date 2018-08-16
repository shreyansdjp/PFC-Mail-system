from mysql import get_connection
import datetime


class Mail:

    @staticmethod
    def get_received_mails(email_id):
        connection = get_connection()
        results = []
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM mail_to WHERE email_id = '%s'" % email_id)
            fetched_mails = cursor.fetchall()
            cursor.close()
        with connection.cursor() as cursor:
            for mail in fetched_mails:
                cursor.execute("SELECT * FROM mails WHERE mail_id = %s" % mail['mail_id'])
                result = cursor.fetchall()
                results.append({
                    'mail_id': result[0]['mail_id'],
                    'from': result[0]['email_id'],
                    'message': result[0]['message'],
                    'subject': result[0]['subject'],
                    'send_at': result[0]['send_at'],
                    'is_read': mail['is_read'],
                })
            connection.close()
            return results

    @staticmethod
    def get_archive_mails(email_id):
        connection = get_connection()
        results = []
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM mail_to WHERE email_id = '%s' and is_archive = 1" % email_id)
            fetched_mails = cursor.fetchall()
            cursor.close()
        with connection.cursor() as cursor:
            for mail in fetched_mails:
                cursor.execute("SELECT * FROM mails WHERE mail_id = %s" % mail['mail_id'])
                result = cursor.fetchall()
                results.append({
                    'mail_id': result[0]['mail_id'],
                    'from': result[0]['email_id'],
                    'message': result[0]['message'],
                    'subject': result[0]['subject'],
                    'send_at': result[0]['send_at'],
                    'is_read': mail['is_read'],
                })
            connection.close()
            return results



    @staticmethod
    def get_sent_mails(email_id):
        connection = get_connection()
        results = []
        with connection.cursor() as cursor:
            cursor.execute("SELECT mail_id, email_id, message, subject, send_at FROM mails WHERE email_id = '%s'" % email_id)
            fetched_mails = cursor.fetchall()
            cursor.close()
        with connection.cursor() as cursor:
            for mail in fetched_mails:
                cursor.execute("SELECT email_id FROM mail_to WHERE mail_id = %s" % mail['mail_id'])
                result = cursor.fetchall()
                results.append({
                    'mail_id': mail['mail_id'],
                    'to': result[0]['email_id'],
                    'subject': mail['subject'],
                    'message': mail['message'],
                    'send_at': mail['send_at']
                })
            connection.close()
            return results

    @staticmethod
    def get_mail(mail_id):
        connection = get_connection()
        result = []
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM mails WHERE mail_id = %s" % mail_id)
            data = cursor.fetchall()
            if data[0]['attachment_id'] is None:
                cursor.execute("SELECT email_id FROM mail_to WHERE mail_id = %s" % mail_id)
                result.append({
                    'from': data[0]['email_id'],
                    'to': cursor.fetchall()[0]['email_id'],
                    'subject': data[0]['subject'],
                    'message': data[0]['message'],
                    'file': None,
                    'send_at': data[0]['send_at']
                })
            else:
                sql = "SELECT file_path FROM attachments WHERE id = %s" % data[0]['attachment_id']
                cursor.execute(sql)
                file_paths = cursor.fetchall()
                cursor.execute("SELECT email_id FROM mail_to WHERE mail_id = %s" % mail_id)
                result.append({
                    'from': data[0]['email_id'],
                    'to': cursor.fetchall()[0]['email_id'],
                    'subject': data[0]['subject'],
                    'message': data[0]['message'],
                    'file': file_paths[0]['file_path'],
                    'send_at': data[0]['send_at']
                })
            connection.close()
            return result

    @staticmethod
    def send_single_mail(email_id_to, email_id_from, subject, tag, message, file=None):
        connection = get_connection()
        if file is None:
            with connection.cursor() as cursor:
                sql = "INSERT INTO mails (email_id, message, subject, tag, send_at, is_read) VALUES ('%s', '%s', '%s', '%s', '%s', %d)" \
                      % (email_id_from, message, subject, tag, str(datetime.datetime.now()), 0)
                cursor.execute(sql)
                connection.commit()
                cursor.close()
            with connection.cursor() as cursor:
                cursor.execute("SELECT mail_id FROM mails ORDER BY mail_id DESC LIMIT 1")
                mail_id = cursor.fetchone()['mail_id']
                cursor.close()
            with connection.cursor() as cursor:
                sql = "INSERT INTO mail_to  VALUES (%s, '%s', 0, 0)" % (mail_id, email_id_to)
                cursor.execute(sql)
                connection.commit()
                connection.close()
                return True
        else:
            attachment_id = Mail().add_files(connection, file)
            with connection.cursor() as cursor:
                sql = "INSERT INTO mails (email_id, message, subject, tag, send_at, attachment_id, is_read) VALUES ('%s', '%s', '%s', '%s', '%s', %s, %d)" \
                      % (email_id_from, message, subject, tag, str(datetime.datetime.now()), attachment_id, 0)
                cursor.execute(sql)
                connection.commit()
                cursor.close()
            with connection.cursor() as cursor:
                cursor.execute("SELECT mail_id FROM mails ORDER BY mail_id DESC LIMIT 1")
                mail_id = cursor.fetchone()['mail_id']
                cursor.close()
            with connection.cursor() as cursor:
                sql = "INSERT INTO mail_to  VALUES (%s, '%s', 0, 0)" % (mail_id, email_id_to)
                cursor.execute(sql)
                connection.commit()
                connection.close()
                return True

    @staticmethod
    def add_files(connection, file_paths):
        with connection.cursor() as cursor:
            sql = "INSERT INTO attachments (file_path) VALUES ('%s')" % file_paths
            cursor.execute(sql)
            connection.commit()
            cursor.execute("SELECT id FROM attachments ORDER BY id DESC LIMIT 1")
            attachment_id = cursor.fetchone()['id']
            return attachment_id

    @staticmethod
    def send_multiple_mail(emails_to, email_id_from, subject, tag, message, file=None):
        connection = get_connection()
        if file is None:
            with connection.cursor() as cursor:
                sql = "INSERT INTO mails (email_id, message, subject, tag, send_at, is_read) VALUES ('%s', '%s', '%s', '%s', '%s', %d)" \
                      % (email_id_from, message, subject, tag, str(datetime.datetime.now()), 0)
                cursor.execute(sql)
                connection.commit()
                cursor.close()
            with connection.cursor() as cursor:
                cursor.execute("SELECT mail_id FROM mails ORDER BY mail_id DESC LIMIT 1")
                mail_id = cursor.fetchone()['mail_id']
                cursor.close()
            with connection.cursor() as cursor:
                for email_id_to in emails_to:
                    sql = "INSERT INTO mail_to VALUES (%s, '%s', 0, 0)" % (mail_id, email_id_to)
                    cursor.execute(sql)
                    connection.commit()
                connection.close()
                return True
        else:
            attachment_id = Mail().add_files(connection, file)
            with connection.cursor() as cursor:
                sql = "INSERT INTO mails (email_id, message, subject, tag, send_at, attachment_id, is_read) VALUES ('%s', '%s', '%s', '%s', '%s', %s, %d)" \
                      % (email_id_from, message, subject, tag, str(datetime.datetime.now()), attachment_id, 0)
                cursor.execute(sql)
                connection.commit()
                cursor.close()
            with connection.cursor() as cursor:
                cursor.execute("SELECT mail_id FROM mails ORDER BY mail_id DESC LIMIT 1")
                mail_id = cursor.fetchone()['mail_id']
                cursor.close()
            with connection.cursor() as cursor:
                for email_id_to in emails_to:
                    sql = "INSERT INTO mail_to VALUES (%s, '%s', 0, 0)" % (mail_id, email_id_to)
                    cursor.execute(sql)
                    connection.commit()
                connection.close()
                return True
