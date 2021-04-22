from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Готово')
