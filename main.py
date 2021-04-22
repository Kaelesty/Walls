from flask import Flask, url_for, render_template
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.utils import redirect

from data import db_session

from forms.loginform import LoginForm
from forms.registerform import RegisterForm
from forms.newdialogueform import NewDialogueForm
from forms.chatform import ChatForm
from forms.newchatform import NewChatForm
from forms.adduserform import UserForm

from data.users import User
from data.messages import Message_l1, Message_l2
from data.dialogues import Dialogue
from data.chats import Chat

import json


app = Flask(__name__)
app.secret_key = "secret"
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/default_pattern")
def render_default():
    return render_template('default.html', _logo=url_for('static', filename=f'images/hat_logo.PNG'), styles=url_for('static', filename='styles/styles.css'))


@app.route("/welcome")
def render_welcome():
    return render_template('welcome.html', _logo=url_for('static', filename=f'images/hat_logo.PNG'), styles=url_for('static', filename='styles/styles.css'))


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
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, styles=url_for('static', filename='styles/styles.css'), _logo=url_for('static', filename=f'images/hat_logo.PNG'))
    return render_template('login.html', title='Авторизация', form=form, _logo=url_for('static', filename=f'images/hat_logo.PNG'), styles=url_for('static', filename='styles/styles.css'))


@app.route('/')
def render_main():
    return render_template('main.html', _logo=url_for('static', title="ChatY", filename=f'images/hat_logo.PNG'), styles=url_for('static', filename='styles/styles.css'))


@app.route('/register', methods=['POST', 'GET'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть", _logo=url_for('static', filename=f'images/hat_logo.PNG'), styles=url_for('static', filename='styles/styles.css'))
        user = User()
        user.name = form.name.data
        user.login = form.login.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, _logo=url_for('static', filename=f'images/hat_logo.PNG'), styles=url_for('static', filename='styles/styles.css'))


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
                                   form=form, message="Пользователь не найден", styles=url_for('static', filename='styles/styles.css'), _logo=url_for('static', filename=f'images/hat_logo.PNG'))
    return render_template('new_dialogue_form.html', title='Новый диалог', form=form, _logo=url_for('static', filename=f'images/hat_logo.PNG'), styles=url_for('static', filename='styles/styles.css'))


@app.route('/new_chat', methods=['POST', 'GET'])
def render_nc():
    form = NewChatForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        query = db_sess.query(Chat).filter(Chat.name == form.name.data)
        if not query.all():
            chat = Chat()
            chat.creator_id = current_user.id
            chat.name = form.name.data
            chat.users = ''
            db_sess.add(chat)
            db_sess.commit()
            return redirect('/')
        else:
            return render_template('new_dialogue_form.html', title='Новый диалог',
                                   form=form, message="Название уже занято", styles=url_for('static', filename='styles/styles.css'), _logo=url_for('static', filename=f'images/hat_logo.PNG'))
    return render_template('new_dialogue_form.html', title='Новый диалог', form=form, _logo=url_for('static', filename=f'images/hat_logo.PNG'), styles=url_for('static', filename='styles/styles.css'))


@app.route('/dialogues/<username>', methods=['POST', 'GET'])
def render_dialogues(username):
    db_sess = db_session.create_session()
    comrade = db_sess.query(User).filter(User.name == username).first()
    avaliable_dialogues = db_sess.query(Dialogue).filter((Dialogue.first_user == current_user) | (Dialogue.second_user == current_user))
    for elem in avaliable_dialogues:
        if (elem.first_user == current_user and elem.second_user == comrade) or \
                (elem.second_user == current_user and elem.first_user == comrade):
            current_dialogue = elem
    form = ChatForm()
    if form.validate_on_submit():
        message = Message_l1()
        message.text = form.text.data
        message.sender_id = current_user.id
        message.dialogue_id = current_dialogue.id
        db_sess.add(message)
        db_sess.commit()
        messages = db_sess.query(Message_l1).filter(Message_l1.dialogue == current_dialogue).all()
        form.text.data = ""
        return render_template('dialogues.html', title='Диалоги',
                               _logo=url_for('static', filename=f'images/hat_logo.PNG'), styles=url_for('static', filename='styles/styles.css'),
                               dialogues=avaliable_dialogues.all(), messages=messages, comrade=comrade, form=form)
    messages = db_sess.query(Message_l1).filter(Message_l1.dialogue == current_dialogue).all()
    return render_template('dialogues.html', title='Диалоги',
                           _logo=url_for('static', filename=f'images/hat_logo.PNG'), styles=url_for('static', filename='styles/styles.css'),
                           dialogues=avaliable_dialogues.all(), messages=messages, comrade=comrade, form=form)


@app.route('/chats/<chatname>', methods=['POST', 'GET'])
def render_chats(chatname):
    db_sess = db_session.create_session()
    avaliable_dialogues = db_sess.query(Chat).filter(
        (Chat.users.like(f"% {current_user.id} %") | (Chat.creator_id == current_user.id)))
    current_dialogue = db_sess.query(Chat).filter((Chat.name == chatname)).first()
    form = ChatForm()
    if form.validate_on_submit():
        message = Message_l2()
        message.text = form.text.data
        message.sender_id = current_user.id
        message.chat_id = current_dialogue.id
        db_sess.add(message)
        db_sess.commit()
        messages = db_sess.query(Message_l2).filter(Message_l2.chat == current_dialogue).all()
        form.text.data = ""
        return render_template('chats.html', title='Диалоги',
                               _logo=url_for('static', filename=f'images/hat_logo.PNG'), styles=url_for('static', filename='styles/styles.css'),
                               chats=avaliable_dialogues.all(), messages=messages, form=form, current_chat=current_dialogue)
    messages = db_sess.query(Message_l2).filter(Message_l2.chat == current_dialogue).all()
    return render_template('chats.html', title='Диалоги',
                           _logo=url_for('static', filename=f'images/hat_logo.PNG'), styles=url_for('static', filename='styles/styles.css'),
                           chats=avaliable_dialogues.all(), messages=messages, form=form, current_chat=current_dialogue)


@app.route('/chats/add_user/<chatname>', methods=['POST', 'GET'])
def render_add_user(chatname):
    form = UserForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == form.name.data)
        chats = db_sess.query(Chat).filter(Chat.name == chatname).first()
        if user.all() and f" {user.first().id} " not in chats.users:
            chats.users = chats.users + f" {user.first().id} "
            db_sess.commit()
            return redirect(f'/chats/{chatname}')
        else:
            return render_template('new_dialogue_form.html', title='Добавление пользователя', form=form,
                                   _logo=url_for('static', filename=f'images/hat_logo.PNG'),
                                   styles=url_for('static', filename='styles/styles.css'), message="Ошибка при добавлении")
    return render_template('new_dialogue_form.html', title='Добавление пользователя', form=form,
                           _logo=url_for('static', filename=f'images/hat_logo.PNG'), styles=url_for('static', filename='styles/styles.css'))


@app.route('/dialogues_redirect', methods=['POST', 'GET'])
def dialogues_redirect():
    db_sess = db_session.create_session()
    dialogue = db_sess.query(Dialogue).filter(
        (Dialogue.first_user == current_user) | (Dialogue.second_user == current_user)).first()
    if dialogue is None:
        return redirect("/new_dialogue")
    elif dialogue.first_user == current_user:
        return redirect(f"/dialogues/{dialogue.second_user.name}")
    else:
        return redirect(f"/dialogues/{dialogue.first_user.name}")


@app.route('/chats_redirect', methods=['POST', 'GET'])
def chats_redirect():
    db_sess = db_session.create_session()
    chat = db_sess.query(Chat).filter((Chat.creator_id == current_user.id) | Chat.users.like(f" %{current_user.id}% ")).first()
    if chat is None:
        return redirect("/new_chat")
    return redirect(f"/chats/{chat.name}")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/welcome")


@app.route("/api/get/<user>/<content>", methods=['GET'])
def api_get(user, content):
    """
    :param user: login&pass (Example: /kayris&123/)
    :param content: content_type (dialogues, chats) (Example: /dialogues)
    :return: json with main key "result", contains user_login, user_name and "content"
            (type of error or list with requested content)
    """
    login, password = user.split("&")[0], user.split("&")[1]
    result = {}
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.login == login).first()
    if not user:
        result["result"] = {
            "user_login": login,
            "user_name": "",
            "content": ["ERROR - WRONG USER"]
        }
        return result
    if user.check_password(password):
        result["result"] = {
            "user_login": user.login,
            "user_name": user.name,
            "user_id": user.id,
            "content": []
        }
        if content == "dialogues":
            dialogues = db_sess.query(Dialogue).filter(
                (Dialogue.first_user_id == user.id) | (Dialogue.second_user_id == user.id)).all()
            for i in range(len(dialogues)):
                dialogues[i] = dialogues[i].to_dict()
            result["result"]["content"] = dialogues
        elif content == "chats":
            chats = db_sess.query(Chat).filter(Chat.users.like(f"% {user.id} %") | (Chat.creator_id == user.id)).all()
            for i in range(len(chats)):
                chats[i] = chats[i].to_dict()
            result["result"]["content"] = chats
        else:
            result["result"]["content"] = ["ERROR - WRONG CONTENT"]
        return result
    else:
        result["result"] = {
            "user_login": login,
            "user_name": "",
            "content": ["ERROR - WRONG PASSWORD"]
        }
        return result


@app.route("/api/post/<user>/<content_type>/<content>", methods=['POST', "GET"])
def api_post(user, content_type, content):
    """
    :param user: login&pass (Example: /kayris&123/)
    :param content_type: type of posting content (message_l1, message_l2)
    :param content:
        FOR message_l1: dialogue_id&text (Example: 32%TEXT~TEST)
        FOR message_l2: chat_id&text (Example: 32%TEXT~TEST)
        !!WARN!! ~ MUST used as SPACES. During posting it will be automatically replaced
    :return: json with main key "result", contains user_login, user_name and "content" (type of error or success message)
    """
    login, password = user.split("&")[0], user.split("&")[1]
    dialogue_id, text = content.split("&")[0], content.split("&")[1]
    result = {}
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.login == login).first()
    if not user:
        result["result"] = {
            "user_login": login,
            "user_name": "",
            "content": ["ERROR - WRONG USER"]
        }
        return result
    if user.check_password(password):
        result["result"] = {
            "user_login": user.login,
            "user_name": user.name,
            "user_id": user.id,
            "content": []
        }
        if content_type == "message_l1":
            dialogue = db_sess.query(Dialogue).filter(Dialogue.id == dialogue_id).first()
            if not dialogue:
                result["result"]["content"] = ["ERROR - DIALOGUE NOT FOUND"]
                return result
            message = Message_l1()
            message.sender_id = user.id
            message.dialogue_id = dialogue.id
            message.text = " ".join(text.split("~"))
            db_sess.add(message)
            db_sess.commit()
            result["result"]["content"] = ["SUCCESS"]
            return result
        elif content_type == "message_l1":
            dialogue = db_sess.query(Chat).filter(Chat.id == dialogue_id).first()
            if not dialogue:
                result["result"]["content"] = ["ERROR - DIALOGUE NOT FOUND"]
                return result
            message = Message_l2()
            message.sender_id = user.id
            message.chat_id = dialogue.id
            message.text = " ".join(text.split("~"))
            db_sess.add(message)
            db_sess.commit()
            result["result"]["content"] = ["SUCCESS"]
            return result
        else:
            result["result"]["content"] = ["ERROR - WRONG CONTENT_TYPE"]
            return result
    else:
        result["result"] = {
            "user_login": login,
            "user_name": "",
            "content": ["ERROR - WRONG PASSWORD"]
        }
        return result

if __name__ == '__main__':
    db_session.global_init("db/data.sqlite")
    app.run(port=8080, host='127.0.0.1')