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
import pandas as pd
import os
import time




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

csv_path = 'utility_matrix.csv'
exit_blog = False

'''
Utility matrix - Recsystem
'''

def init_or_update_csv():

    df = pd.read_csv(csv_path)
    num_cols = len(df.columns)
    num_rows = len(df.index)
    
    num_users = Users.query.count()
    num_blogs = Blogs.query.count()
        
    if num_users > num_cols:
        temp_col = [0] * num_rows
        temp_col = pd.DataFrame(temp_col)
        df = pd.concat([df, temp_col], axis=1)
        df = df.to_numpy()
        df = pd.DataFrame(df)
        df.to_csv(csv_path, index=False)

    if num_blogs > num_rows:
        df = df.T
        df.to_csv(csv_path, index=False)
        df = pd.read_csv(csv_path)
        num_rows = len(df.index)
        
        temp_col = [0] * num_rows
        temp_col = pd.DataFrame(temp_col)
        df = pd.concat([df, temp_col], axis=1)
        df = df.T.to_numpy()
        df = pd.DataFrame(df)
        df.to_csv(csv_path, index=False)
        
        
def fill_uitlity_matrix(blog_id, user_id, duration):
    df = pd.read_csv(csv_path)
    df.iloc[blog_id - 1][user_id - 1] = duration
    df.to_csv(csv_path, index=False)

def delete_row_utility_matrix(blog_id):
    df = pd.read_csv(csv_path)
    df = df.drop([blog_id-1])
    df.to_csv(csv_path, index=False)
    
'''
RecSys
'''
def cosine(a, b):
    # add the epsilon to avoid denominator being 0
    return a.dot(b) / ((np.linalg.norm(a) * np.linalg.norm(b)) + np.finfo(np.float64).eps)

# function in flask backend
def compute(current_user_logined_id):
    utility_matrix = pd.read_csv("utility_matrix.csv")
    utility_matrix.replace(0, np.nan, inplace=True)
    mean = utility_matrix.mean(skipna=True)
    utility_matrix = utility_matrix.sub(mean, axis=1)
    utility_matrix = utility_matrix.fillna(0)
    utility_matrix = utility_matrix.values

    num_user = utility_matrix.shape[1]
    user_to_user_similarity_matrix = np.zeros((num_user, num_user))

    for i in range(num_user):
      for j in range(num_user):
        user_i = utility_matrix[:,i]
        user_j = utility_matrix[:,j]
        index_not_zero = (user_i > 0) & (user_j > 0)
        user_to_user_similarity_matrix[i,j] = cosine(user_i[index_not_zero], user_j[index_not_zero])
      
    zero_rating_indices = np.where(utility_matrix == 0)
    for blog, user in zip(zero_rating_indices[0], zero_rating_indices[1]):
      similar_users = user_to_user_similarity_matrix[user]
      blog_time_spent = utility_matrix[blog]
      index = blog_time_spent > 0
      blog_time_spent = blog_time_spent[index]
      similar_users = similar_users[index]
      utility_matrix[blog, user] = np.sum(blog_time_spent * similar_users) / (np.sum(similar_users) + np.finfo(np.float64).eps)

    mean = mean.values
    utility_matrix = utility_matrix + mean
    utility_matrix = pd.DataFrame(utility_matrix)
    utility_matrix.to_csv("filled_utility_matrix.csv", index=False) 

    utility_matrix = pd.read_csv("utility_matrix.csv")
    utility_matrix_filled = pd.read_csv("filled_utility_matrix.csv")

    zero_rating_indices = np.where(utility_matrix == 0)
    dictionary = {}
    for blog, user in zip(zero_rating_indices[0], zero_rating_indices[1]):
        if user == current_user_logined_id - 1:
          dictionary[blog + 1] = utility_matrix_filled.iloc[blog, user]
        
    dictionary = sorted(dictionary.items(), key=lambda item: item[1], reverse=True)
    threshold = mean[current_user_logined_id - 1]
    result = [i for i, j in dictionary if j >= threshold]
    return result[:3]
    
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
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    

'''
Form 
'''
from form_backup import Registration, Login, PostBlogForm, UpdateBlogForm, UpdateInfo, SearchForm


'''
Search Function 
'''
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@app.route("/search", methods=["POST"])
def search():
    form = SearchForm()
    blogs = Blogs.query
    if form.validate_on_submit():
        searched = form.searched.data
        blogs = blogs.filter(Blogs.content.like('%' + searched + '%'))
        blogs = blogs.order_by(Blogs.title).all()
        
        return render_template("search.html", form=form, searched=searched, blogs=blogs)

    
'''
Route 
'''
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/recsys")
def recsys():
    result = compute(current_user_logined_id=current_user.id)
    all_blogs = Blogs.query.order_by(Blogs.date_posted)
    return render_template("recsys.html", result=result, all_blogs=all_blogs)

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
            # init_or_update_csv()

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
                     )
        db.session.add(post)
        db.session.commit()
        
        
        title = form.title.data
        form.title.data = ''
        form.content.data = ''
        
        init_or_update_csv()
        return redirect(url_for('dashboard', id=current_user.id))
              
    return render_template("create_blog.html", title=title, form=form)

@app.route("/all_blogs")
def all_blogs():
    all_blogs = Blogs.query.order_by(Blogs.date_posted)
    return render_template("all_blogs.html", all_blogs=all_blogs)


def convert_to_sec(time_to_convert):
    format_str = "%H:%M:%S"
    time_struct = time.strptime(time_to_convert, format_str)
    hour = time_struct.tm_hour
    minute = time_struct.tm_min
    second = time_struct.tm_sec
    seconds = hour * 3600 + minute * 60 + second
    return seconds

@app.route("/time/<int:start_time_sec>/<int:id>", methods=["GET", "POST"])
def time(start_time_sec, id):
    end_time = datetime.utcnow()
    end_time_str = end_time.strftime("%H:%M:%S")
    end_time_sec = convert_to_sec(end_time_str)
    duration = end_time_sec - start_time_sec
    
    num_users = Users.query.count()
    num_blogs = Blogs.query.count()
    
    fill_uitlity_matrix(id, current_user.id, duration)
    return redirect(url_for('all_blogs'))

import time
@app.route("/blog/<int:id>")
def blog(id):
    blog = Blogs.query.get_or_404(id)
    start_time = datetime.utcnow()
    start_time_str = start_time.strftime("%H:%M:%S")
    start_time_sec = convert_to_sec(start_time_str)
    print(start_time_sec)
    return render_template('blog.html', blog=blog, start_time_sec=start_time_sec, datetime=datetime)

@app.route("/all_blogs/edit_blog/<int:id>", methods=["GET", "POST"])
@login_required
def edit_blog(id):
    blog = Blogs.query.get_or_404(id)
    form = UpdateBlogForm()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.content = form.content.data

        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('blog', id=blog.id))

    form.title.data = blog.title
    form.content.data = blog.content
    return render_template('edit_blog.html', form=form, blog=blog)

@app.route("/delete_blog/<int:id>", methods=["GET", "POST"])
def delete_blog(id):
    blog_to_delete = Blogs.query.get_or_404(id)
    try:
        db.session.delete(blog_to_delete)
        db.session.commit()
        delete_row_utility_matrix(id)
        return redirect(url_for('dashboard', id=current_user.id))
    except:
        return redirect(url_for('dashboard', id=current_user.id))
        
@app.route("/other_user_blogs/<int:id>", methods=["GET", "POST"])
def other_user_blogs(id):
    user = Users.query.get_or_404(id)
    all_blogs = Blogs.query.order_by(Blogs.date_posted)
    return render_template('other_user_blogs.html', user=user, all_blogs=all_blogs)

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
    