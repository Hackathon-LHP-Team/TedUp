from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, EqualTo, Length

class Registration(FlaskForm):
    name = StringField("Enter name:", validators=[DataRequired()])
    email = StringField("Enter email:", validators=[DataRequired()])
    user_name = StringField("Enter displayed name:", validators=[DataRequired()])
    password_hash = PasswordField("Enter password:", validators=[DataRequired(), EqualTo('password_hash2', message='Password Must Match')])
    password_hash2 = PasswordField("Confirm password:", validators=[DataRequired()])
    submit = SubmitField("Register now")   
    
class Login(FlaskForm):
    email = StringField("Enter your email:", validators=[DataRequired()])
    password_hash = PasswordField("Enter your password:", validators=[DataRequired()])
    submit = SubmitField("Login now")   
    
class PostBlogForm(FlaskForm):
    title = StringField("Enter Title:", validators=[DataRequired()])
    content = StringField("Enter Content:", validators=[DataRequired()], widget=TextArea())
    slug = StringField("Enter slug", validators=[DataRequired()])
    submit = SubmitField("Post now")   
    
class UpdateInfo(FlaskForm):
    name = StringField("Enter name:", validators=[DataRequired()])
    email = StringField("Enter email:", validators=[DataRequired()])
    user_name = StringField("Enter displayed name:", validators=[DataRequired()])
    submit = SubmitField("Update now")   