import os
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from functools import wraps
from classes.user import User
from classes.mail import Mail

UPLOAD_FOLDER = 'attachments'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'xlsx', 'ppt']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'something i know'

# handle errors in mysql execute statements
# add required field in html and remove novalidate from all of it.

TAGS = ['accounts', 'sales', 'higher management']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'name' in session and 'email_id' in session:
            return f(*args, **kwargs)
        else:
            session['error'] = None
            return redirect(url_for('index'))
    return wrap


def is_signed_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'name' in session and 'email_id' in session:
            return redirect(url_for('mail'))
        else:
            return f(*args, **kwargs)
    return wrap


def is_user_related(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        return f(*args, **kwargs)
    return wrap


def is_empty(string):
    if not string:
        return True
    return False


@app.route('/attachments/<filename>')
@is_logged_in
@is_user_related
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/')
@is_signed_in
def index():
    if 'error' not in session:
        return render_template('index.html', loginError=None)
    else:
        return render_template('index.html', loginError=session['error'])


@app.route('/login', methods=['POST'])
def login():
    email_id = request.form['email']
    password = request.form['password']
    logged_in = User().login(email_id, password)
    if logged_in[0] is True:
        session['name'] = logged_in[1]['name']
        session['email_id'] = logged_in[1]['email_id']
        return redirect(url_for('mail'))
    else:
        session['error'] = logged_in[1]
        return redirect(url_for('index'))


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/mail')
@is_logged_in
def mail():
    mails = Mail().get_received_mails(session['email_id'])
    return render_template('mail.html', mails=mails, name=session['name'])


@app.route('/mail/<string:box>')
@is_logged_in
def mailing_box(box):
    mails = Mail().get_received_mails(session['email_id'])
    return render_template('boxmails.html', box=box, mails=mails, name=session['name'])


@app.route('/mail/<box>/id/<mail_id>')
@is_logged_in
def show_email(box, mail_id):
    return render_template('email.html', box=box, mail=Mail().get_mail(mail_id))


@app.route('/sent')
@is_logged_in
def sent_mail():
    sent_mails = Mail().get_sent_mails(session['email_id'])
    return render_template('sent.html', mails=sent_mails, name=session['name'])


@app.route('/archives')
@is_logged_in
def archive_mails():
    return render_template('archives.html', mails=Mail().get_archive_mails(session['email_id']), name=session['name'])


@app.route('/compose', methods=["GET", "POST"])
@is_logged_in
def compose():
    if request.method == 'POST':
        files = request.files.getlist('file')
        emails = request.form.getlist('email')
        subject = request.form['subject']
        body = request.form['body']
        tag = request.form['tag'].lower()
        if len(emails) == 1:
            if User().check_email_id(emails[0]):
                if not (tag in TAGS):
                    message = 'Enter a valid tag (Accounts, Sales, Higher Management)'
                    classes = 'danger'
                    return render_template('compose.html', message=message, classes=classes)
                if len(files) == 0:
                    if Mail().send_single_mail(emails[0], session['email_id'], subject, tag, body):
                        message = 'Mail sent successfully!'
                        classes = 'success'
                        return render_template('compose.html', message=message, classes=classes)
                    else:
                        message = 'Something went wrong while sending mail'
                        classes = 'danger'
                        return render_template('compose.html', message=message, classes=classes)
                elif len(files) >= 1:
                    file_paths = []
                    for file in files:
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                        file_paths.append(file.filename)
                    file_paths = "!".join(file_paths)
                    if Mail().send_single_mail(emails[0], session['email_id'], subject, tag, body, file=file_paths):
                        message = 'Mail sent successfully!'
                        classes = 'success'
                        return render_template('compose.html', message=message, classes=classes)
                    else:
                        message = 'Something went wrong while sending mail'
                        classes = 'danger'
                        return render_template('compose.html', message=message, classes=classes)
            else:
                message = 'Email that you entered did not match'
                classes = 'danger'
                return render_template('compose.html', message=message, classes=classes)
        elif len(emails) > 1:
            for email in emails:
                if not User().check_email_id(email):
                    message = email + ' that you entered did not match'
                    classes = 'danger'
                    return render_template('compose.html', message=message, classes=classes)
            if not (tag in TAGS):
                message = 'Enter a valid tag (Accounts, Sales, Higher Management)'
                classes = 'danger'
                return render_template('compose.html', message=message, classes=classes)
            if len(files) == 0:
                if Mail().send_multiple_mail(emails, session['email_id'], subject, tag, body):
                    message = 'Mail sent successfully!'
                    classes = 'success'
                    return render_template('compose.html', message=message, classes=classes)
                else:
                    message = 'Something went wrong while sending mail'
                    classes = 'danger'
                    return render_template('compose.html', message=message, classes=classes)
            elif len(files) >= 1:
                file_paths = []
                for file in files:
                    file.save(os.path.join(file.filename))
                    file_paths.append(file.filename)
                file_paths = "!".join(file_paths)
                if Mail().send_multiple_mail(emails, session['email_id'], subject, tag, body, file=file_paths):
                    message = 'Mail sent successfully!'
                    classes = 'success'
                    return render_template('compose.html', message=message, classes=classes)
                else:
                    message = 'Something went wrong while sending mail'
                    classes = 'danger'
                    return render_template('compose.html', message=message, classes=classes)
    elif request.method == 'GET':
        message = None
        classes = None
        return render_template('compose.html', message=message, classes=classes)


if __name__ == '__main__':
    app.run(port=2000, debug=True)
