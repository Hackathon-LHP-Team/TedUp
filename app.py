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
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user


'''
Define key and variables
'''
app = Flask(__name__)
app.config["SECRET_KEY"] = "hackathon_round_2" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

'''
Database
'''
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email =  db.Column(db.String(120), nullable=False, unique=True)
    user_name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(200))
    posts = db.relationship('Blogs', backref='poster')
    
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
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    

'''
Form 
'''
from form_backup import Registration, Login, PostBlogForm, UpdateBlogForm, UpdateInfo
 
    
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
        return redirect(url_for('login'))
    all_users = Users.query.order_by(Users.date_added)
    return render_template("registration.html", form=form, name=name, all_users=all_users)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    form = Login()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password_hash.data):
                login_user(user)
                return redirect(url_for('all_users'))
            else:
                flash('Wrong password. Please try again')
        else:
            flash('User does not exist. Please sign up to create an account')
    return render_template("login.html", form=form)


@app.route("/all_users", methods=["GET", "POST"])   
@login_required 
def all_users():
    all_users = Users.query.order_by(Users.date_added)
    return render_template("all_users.html", all_users=all_users)

@app.route("/dashboard/<int:id>", methods=["GET", "POST"])   
@login_required 
def dashboard(id):
    user = Users.query.get_or_404(id)
    all_blogs = Blogs.query.order_by(Blogs.date_posted)
    return render_template('dashboard.html', user=user, all_blogs=all_blogs)

@app.route("/dashboard/update_info/<int:id>", methods=["GET", "POST"])
@login_required
def update_info(id):
    user = Users.query.get_or_404(id)
    form = UpdateInfo()
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.user_name = form.user_name.data

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('dashboard', id=user.id))

    form.name.data = user.name
    form.email.data = user.email
    form.user_name.data = user.user_name
    return render_template('update_info.html', form=form, user=user)
    
@app.route("/create_blog", methods=["GET", "POST"]) 
@login_required
def create_blog():
    title = None
    form = PostBlogForm()
    if form.validate_on_submit():
        poster = current_user.id
        post = Blogs(title=form.title.data,
                     poster_id = poster,
                     content=form.content.data,
                     slug=form.slug.data
                     )
        db.session.add(post)
        db.session.commit()
        
        title = form.title.data
        form.title.data = ''
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


@app.route("/blog/<int:id>")
def blog(id):
    blog = Blogs.query.get_or_404(id)
    return render_template('blog.html', blog=blog)

@app.route("/all_blogs/edit_blog/<int:id>", methods=["GET", "POST"])
@login_required
def edit_blog(id):
    blog = Blogs.query.get_or_404(id)
    form = UpdateBlogForm()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.content = form.content.data
        blog.slug = form.slug.data

        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('blog', id=blog.id))

    form.title.data = blog.title
    form.content.data = blog.content
    form.slug.data = blog.slug
    return render_template('edit_blog.html', form=form, blog=blog)

@app.route("/blog/delete_blog/<int:id>", methods=["GET", "POST"])
def delete_blog(id):
    blog_to_delete = Blogs.query.get_or_404(id)
    try:
        db.session.delete(blog_to_delete)
        db.session.commit()
        list_index = list (range (1, 8)) 
        random.shuffle (list_index) 
        list_index_str = ["avatar_" + str(index) for index in list_index]
        all_blogs = Blogs.query.order_by(Blogs.date_posted)
        return render_template("all_blogs.html", all_blogs=all_blogs, list_index_str=list_index_str, zip=zip)
    except:
        flash("Something went wrong, please reload and try again")
        list_index = list (range (1, 8)) 
        random.shuffle (list_index) 
        list_index_str = ["avatar_" + str(index) for index in list_index]
        all_blogs = Blogs.query.order_by(Blogs.date_posted)
        return render_template("all_blogs.html", all_blogs=all_blogs, list_index_str=list_index_str, zip=zip)
        
        

@app.route("/download")
def download():
    return render_template("download.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
 
 
 







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
    