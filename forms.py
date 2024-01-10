from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(4, 30)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(4, 30)])
    mail = StringField('Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm')])
    confirm = PasswordField('Confirm password')
    submit = SubmitField('Sign Up')


class VerificationForm(FlaskForm):
    code = StringField(validators=[DataRequired(), Length(6, 6)])
    submit = SubmitField('Send')
