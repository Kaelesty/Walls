from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NewChatForm(FlaskForm):
    name = StringField('Название Беседы:', validators=[DataRequired()])
    submit = SubmitField('Создать')
