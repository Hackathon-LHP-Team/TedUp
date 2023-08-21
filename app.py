# Machine Learning libs
import tensorflow as tf
import numpy as np
import pandas as pd

# Flask Backend Framework
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, send_from_directory, current_app
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from datetime import datetime
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, EqualTo, Length
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

# Other supplemetary libs
import os
import time


# ----------- Keys and Global Variables -----------
app = Flask(__name__)
app.config["SECRET_KEY"] = "hackathon_round_3_LHP_team" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

csv_path = 'utility_matrix.csv'
exit_blog = False

# ----------- Recommender System -----------
from recommender_sytem_backup import utility_matrix_management, recys
util_matrix = utility_matrix_management(csv_path=csv_path)
recys = recys()
    
    
# ----------- Database -----------
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
    
class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    path = db.Column(db.String(256)) # Option 2: store file path
    

# ----------- Form -----------
from form_backup import Registration, Login, PostBlogForm, UpdateBlogForm, UpdateInfo, SearchForm


# ----------- Podcast -----------
@app.route('/create_podcast')
def upload_page():
    return render_template('create_podcast.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and file.filename.endswith('.mp3') and file.content_length < 10 * 1024 * 1024:
        name = f'audio_{Audio.query.count() + 1}.mp3'
        folder = 'static/audio_files'
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, name)
        file.save(path)
        audio = Audio(name=name)
        audio.path = path
        db.session.add(audio)
        db.session.commit()
        return f'File {name} uploaded successfully'
    else:
        return 'Invalid file type or size'

# ----------- Search Function -----------
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

    
# ----------- Route -----------
@app.route("/")
def home():
    return render_template("home.html")


# ----------- Registration and Login -----------
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
            util_matrix.init_or_update_csv(Users_query=Users.query.count(), Blogs_query=Blogs.query.count())

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


# ----------- User and Dashboard -----------
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
    
    
# ----------- Blog management -----------
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
        
        util_matrix.init_or_update_csv(Users_query=Users.query.count(), Blogs_query=Blogs.query.count())
        return redirect(url_for('dashboard', id=current_user.id))
              
    return render_template("create_blog.html", title=title, form=form)

@app.route("/all_blogs")
def all_blogs():
    all_blogs = Blogs.query.order_by(Blogs.date_posted)
    return render_template("all_blogs.html", all_blogs=all_blogs)

@app.route("/recsys")
def recsys():
    result = recys.compute(current_user_logined_id=current_user.id)
    all_blogs = Blogs.query.order_by(Blogs.date_posted)
    return render_template("recsys.html", result=result, all_blogs=all_blogs)

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
    
    util_matrix.fill_uitlity_matrix(blog_id=id, user_id=current_user.id, duration=duration)
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
@login_required
def delete_blog(id):
    blog_to_delete = Blogs.query.get_or_404(id)
    try:
        db.session.delete(blog_to_delete)
        db.session.commit()
        util_matrix.delete_row_utility_matrix(blog_id=id)
        return redirect(url_for('dashboard', id=current_user.id))
    except:
        return redirect(url_for('dashboard', id=current_user.id))
        
@app.route("/other_user_blogs/<int:id>", methods=["GET", "POST"])
def other_user_blogs(id):
    user = Users.query.get_or_404(id)
    all_blogs = Blogs.query.order_by(Blogs.date_posted)
    return render_template('other_user_blogs.html', user=user, all_blogs=all_blogs)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
 
 

# ----------- Additional pages -----------

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
    