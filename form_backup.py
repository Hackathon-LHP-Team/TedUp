from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, EqualTo, Length


class Registration(FlaskForm):
    name = StringField("Enter name", validators=[DataRequired()])
    email = StringField("Enter email", validators=[DataRequired()])
    user_name = StringField("Enter display name", validators=[DataRequired()])
    password_hash = PasswordField("Enter password", validators=[DataRequired(), EqualTo('password_hash2', message='Password Must Match')])
    password_hash2 = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Register now")   
    
class Login(FlaskForm):
    email = StringField("Enter your email", validators=[DataRequired()])
    password_hash = PasswordField("Enter your password", validators=[DataRequired()])
    submit = SubmitField("Login now")   
    
class PostBlogForm(FlaskForm):
    title = StringField("Enter Title", validators=[DataRequired()])
    content = StringField("Enter Content", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Post story now")   
    
class UpdateBlogForm(FlaskForm):
    title = StringField("Enter Title", validators=[DataRequired()])
    content = StringField("Enter Content", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Update story now")   
    
class CommentForm(FlaskForm):
    content = StringField("Comment", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Comment now")  
    
class UpdateInfo(FlaskForm):
    name = StringField("Change name", validators=[DataRequired()])
    email = StringField("Change email", validators=[DataRequired()])
    user_name = StringField("Change display name:", validators=[DataRequired()])
    submit = SubmitField("Update now")   

class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()]) 
    submit = SubmitField("Search now")  

class NewPlaylist(FlaskForm):
    title = StringField("Enter Title", validators=[DataRequired()])
    description = StringField("Enter description", validators=[DataRequired()])
    submit = SubmitField("Upload now")   
    
class NewCategory(FlaskForm):
    title = StringField("Enter Title", validators=[DataRequired()])
    description = StringField("Enter description", validators=[DataRequired()])
    submit = SubmitField("Upload now")  
    
class UploadAudio(FlaskForm):
    title = StringField("Enter Title", validators=[DataRequired()])
    description = StringField("Enter description", validators=[DataRequired()])
    playlist_id = StringField("Enter playlist id", validators=[DataRequired()])
    submit = SubmitField("Upload now")   


    