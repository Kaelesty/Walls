from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Готово')