from flask import Flask, url_for, render_template
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.utils import redirect
from flask import request

from data import db_session
from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from forms.newdialogueform import NewDialogueForm

from data.users import User
from data.messages import Message_l1
from data.dialogues import Dialogue

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
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form, _logo=url_for('static', filename=f'images/hat_logo.PNG'))


@app.route('/')
def render_main():
    return render_template('main.html', _logo=url_for('static', filename=f'images/hat_logo.PNG'))


@app.route('/register', methods=['POST', 'GET'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть", _logo=url_for('static', filename=f'images/hat_logo.PNG'))
        user = User(
            name=form.name.data,
            login=form.login.data,
            hashed_password=form.password.data,
        )
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, _logo=url_for('static', filename=f'images/hat_logo.PNG'))


@app.route('/new_dialogue', methods=['POST', 'GET'])
def render_nd():
    form = NewDialogueForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        query = db_sess.query(User).filter(User.name == form.name.data)
        if query.first() and form.name.data != current_user.name:
            dialogue = Dialogue()
            dialogue.first_user_id = current_user.id
            dialogue.second_user_id = query.first().id
            db_sess.add(dialogue)
            db_sess.commit()
            return redirect('/')
        else:
            return render_template('new_dialogue_form.html', title='Новый диалог',
                                   form=form, message="Пользователь не найден")
    return render_template('new_dialogue_form.html', title='Новый диалог', form=form, _logo=url_for('static', filename=f'images/hat_logo.PNG'))


@app.route('/dialogues/<username>', methods=['POST', 'GET'])
def render_dialogues(username):
    db_sess = db_session.create_session()
    comrade = db_sess.query(User).filter(User.name == username)
    avaliable_dialogues = db_sess.query(Dialogue).filter((Dialogue.first_user == current_user) | (Dialogue.second_user == current_user))
    messages = db_sess.query(Message_l1).filter(Message_l1.dialogue == avaliable_dialogues.first()).all()
    return render_template('dialogues.html', title='Диалоги',
                           _logo=url_for('static', filename=f'images/hat_logo.PNG'), dialogues=avaliable_dialogues.all(), messages=messages)







@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/welcome")

if __name__ == '__main__':
    db_session.global_init("db/data.sqlite")
    app.run(port=8080, host='127.0.0.1')