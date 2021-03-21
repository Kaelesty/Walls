from flask import Flask, url_for, render_template
from flask_login import LoginManager

app = Flask(__name__)


@app.route("/default_pattern")
def render_default():
    return render_template('default.html', _logo=url_for('static', filename=f'images/hat_logo.PNG'))


@app.route("/welcome")
def render_welcome():
    return render_template('welcome.html', _logo=url_for('static', filename=f'images/hat_logo.PNG'))


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')