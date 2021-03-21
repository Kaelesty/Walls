from flask import Flask, url_for, render_template
from flask_login import LoginManager, login_user
from werkzeug.utils import redirect

from data import db_session
from data.login_form import LoginForm
from data.users import User

CRP_MOVE = 17


def encrypt(string):
    string = list(string)
    res = ""
    for i in range(len(string)):
        res += chr(ord(string[i]) + i - CRP_MOVE)
    return res


def decrypt(string):
    string = list(string)
    res = ""
    for i in range(len(string)):
        res += chr(ord(string[i]) - i + CRP_MOVE)
    return res


app = Flask(__name__)
app.secret_key = "secret"
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/default_pattern")
def render_default():
    return render_template('default.html', _logo=url_for('static', filename=f'images/hat_logo.PNG'))


@app.route("/welcome")
def render_welcome():
    return render_template('welcome.html', _logo=url_for('static', filename=f'images/hat_logo.PNG'))


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    db_session.global_init("db/data.sqlite")
    app.run(port=8080, host='127.0.0.1')