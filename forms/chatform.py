from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ChatForm(FlaskForm):
    text = StringField('Логин', validators=[DataRequired()])
    submit = SubmitField('🢂')
