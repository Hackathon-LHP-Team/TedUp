'''
Structure of the web
Homepage
    - Navbar:
        - Logo + Virtual Therapist
        - Developer docs:
            - Documentations (how to clone this website and run code)
            - Github (Deep learning notebook, resources)
            - Research paper
        - About us
        - Experience app
        - Account
    - Main theme:
        - Motion image 
        - "explore now" button
    - Our Story / Introduction (With Virtual Therapist, you've got someone in your corner) -> 4 main features
    - Demo (two options: video or gif image with options bar) -> Small conversation, meaningful progress
    - Core/key features (images needed):
        - Chatbot as virtual therapist
        - Artificial Intelligence using Deep Neural Network 
        - Syetem for Mental health quality assessment
    - Team members
        - Name + task (leader: Idea pitching, AI engineer, Backend developer)
        - Name + task (frontend developers)
        - Name + Task (Persona + Design)
    
App page:
    - Sidebar:
        - Your conversations
        - Your history record
        - System messages
        - Blogs (optional)
'''


import tensorflow as tf
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, send_from_directory, current_app
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from datetime import datetime
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, EqualTo, Length
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import random 

'''
Define key and variables
'''
app = Flask(__name__)
app.config["SECRET_KEY"] = "hackathon_round_2" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

'''
Database
'''
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email =  db.Column(db.String(120), nullable=False, unique=True)
    user_name = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(200))
    @property
    def password():
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify(self, password):
        return check_password_hash(self.password_hash, password)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # Create a string
    def __repr__(self):
        return '<Name %r>' % self.name
    
class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    

'''
Form 
'''
class Registration(FlaskForm):
    name = StringField("Enter your name:", validators=[DataRequired()])
    email = StringField("Enter your email:", validators=[DataRequired()])
    user_name = StringField("Enter your user name:", validators=[DataRequired()])
    password_hash = PasswordField("Enter your password:", validators=[DataRequired(), EqualTo('password_hash2', message='Password Must Match')])
    password_hash2 = PasswordField("Confirm your password:", validators=[DataRequired()])
    submit = SubmitField("Register now")   
    
class PostBlogForm(FlaskForm):
    title = StringField("Title:", validators=[DataRequired()])
    author = StringField("Author:", validators=[DataRequired()])
    content = StringField("Content:", validators=[DataRequired()], widget=TextArea())
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Post now")   
    
'''
Route 
'''
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/registration", methods=["GET", "POST"]) 
def registration():
    name = None
    form = Registration()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None: 
            hased_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(name=form.name.data, email=form.email.data, user_name=form.user_name.data, password_hash=hased_pw)
            db.session.add(user)
            db.session.commit()

        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        form.user_name.data = ""
        form.password_hash.data = ""
        flash("Thank you for joining us!")
    all_users = Users.query.order_by(Users.date_added)
    return render_template("registration.html", form=form, name=name, all_users=all_users)


@app.route("/all_users")
def all_users():
    list_index = list (range (1, 8)) 
    random.shuffle (list_index) 
    list_index_str = ["avatar_" + str(index) for index in list_index]
    all_users = Users.query.order_by(Users.date_added)
    return render_template("all_users.html", all_users=all_users, list_index_str=list_index_str, zip=zip)
    
@app.route("/login")
def login():
    return render_template("login.html")
    
@app.route("/create_blog", methods=["GET", "POST"]) 
def create_blog():
    title = None
    form = PostBlogForm()
    if form.validate_on_submit():
        post = Blogs(title=form.title.data,
                     author=form.author.data,
                     content=form.content.data,
                     slug=form.slug.data
                     )
        db.session.add(post)
        db.session.commit()
        
        title = form.title.data
        form.title.data = ''
        form.author.data = ''
        form.content.data = ''
        form.slug.data = ''
        
        flash("Create a blog post succesfully")
        
    return render_template("create_blog.html", title=title, form=form)

@app.route("/all_blogs")
def all_blogs():
    list_index = list (range (1, 8)) 
    random.shuffle (list_index) 
    list_index_str = ["avatar_" + str(index) for index in list_index]
    all_blogs = Blogs.query.order_by(Blogs.date_posted)
    return render_template("all_blogs.html", all_blogs=all_blogs, list_index_str=list_index_str, zip=zip)

@app.route("/download")
def download():
    return render_template("download.html")
 
 
 







'''
Additional page
'''
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
    