from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,RadioField,TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo,Length

class Login(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignUp(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[Email(), DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password', message=('Password must match'))])
    gender = RadioField('Gender:', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    phone = StringField("Phone no", validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class Contact(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), DataRequired()])
    message = TextAreaField('Message', render_kw={"rows": 70, "cols": 11}, validators=[DataRequired()])
    submit = SubmitField('Send')
