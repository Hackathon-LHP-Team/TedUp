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

# jinja




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
    comments = db.relationship('Comments', backref='commenter')
    reacts = db.relationship('Reactions', backref='reacter')
    bookmarks = db.relationship('BookMarks', backref='bookmarker')
    
    
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
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    blog_commented = db.relationship('Comments', backref='blog_commented')
    blog_reacted = db.relationship('Reactions', backref='blog_reacted')
    tags = db.relationship('Tags', backref='blog_tags')
    blog_bookmarked = db.relationship('BookMarks', backref='blog_bookmarked')
    blog_category = db.relationship('Categories', backref='blog_category')
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
  
class Reactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reaction_type = db.Column(db.String(255), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    reacter_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
    
class BookMarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookmark_state = db.Column(db.String(255), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    bookmarker_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))

class Playlists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    audios = db.relationship('Audio', backref='playlist')
    
class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
    
class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    path = db.Column(db.String(256)) 
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'))
    

# ----------- Form -----------
from form_backup import Registration, Login, PostBlogForm, UpdateBlogForm, UpdateInfo, SearchForm, UploadAudio, CommentForm, NewPlaylist, NewCategory


# ----------- Playlist -----------
@app.route('/new_playlist', methods=["GET", "POST"])
def new_playlist():
    form = NewPlaylist()
    if form.validate_on_submit():
        playlist = Playlists(title=form.title.data,
                           description=form.description.data,
                            )
        db.session.add(playlist)
        db.session.commit()
        form.title.data = ''
        form.description.data = ''
    return render_template('new_playlist.html', form=form)

# ----------- Category -----------
@app.route('/new_category', methods=["GET", "POST"])
def new_category():
    form = NewCategory()
    if form.validate_on_submit():
        category = Categories(title=form.title.data,
                            description=form.description.data,
                            )
        db.session.add(category)
        db.session.commit()
        form.title.data = ''
        form.description.data = ''
    return render_template('new_category.html', form=form)

# ----------- Podcast -----------
@app.route('/create_podcast')
def upload_page():
    form = UploadAudio()
    return render_template('create_podcast.html', form=form)

@app.route('/all_podcasts')
def all_podcasts():
    all_podcasts = Audio.query.order_by(Audio.date_posted)
    playlists = Playlists.query.order_by(Playlists.id)
    return render_template("all_podcasts.html", all_podcasts=all_podcasts, playlists=playlists)

@app.route("/playlist_play/<int:id>", methods=["GET", "POST"])   
def playlist_play(id):
    playlist = Playlists.query.get_or_404(id)
    podcast = Audio.query.filter_by(playlist_id=id).first()
    name = 'audio_files/' + podcast.name 
    all_podcasts = Audio.query.order_by(Audio.date_posted)
    return render_template('playlist_play.html', playlist=playlist, podcast=podcast, name=name, all_podcasts=all_podcasts)

@app.route("/podcast/<int:id>", methods=["GET", "POST"])   
def podcast(id):
    podcast = Audio.query.get_or_404(id)
    playlist = Playlists.query.get_or_404(podcast.playlist_id)
    name = 'audio_files/' + podcast.name 
    all_podcasts = Audio.query.order_by(Audio.date_posted)
    return render_template('podcast.html', podcast=podcast, playlist=playlist, name=name, all_podcasts=all_podcasts)


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and file.content_length < 10 * 1024 * 1024:
        name = f'audio_{Audio.query.count() + 1}.mp3'
        folder = 'static/audio_files'
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, name)
        file.save(path)
        # Get the title and description from the form
        title = request.form.get('title')
        description = request.form.get('description')
        playlist_id = request.form.get('playlist_id')
        # Create the audio object with the title and description
        audio = Audio(name=name, title=title, description=description, playlist_id=playlist_id)
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
                return redirect(url_for('cold_start', id=current_user.id))
            else:
                flash('Wrong password. Please try again')
        else:
            flash('User does not exist. Please sign up to create an account')
    return render_template("login.html", form=form)

@app.route("/cold_start/<int:id>", methods=["GET", "POST"])
def cold_start(id):
    tags = Tags.query.order_by(Tags.date_posted)
    list_tags = ["cảm xúc", "chủng tộc", "sở thích", "du lịch", "thể thao", "hẹn hò", "gia đình", "đồng nghiệp", "bạn bè", "tâm lý", "nhân cách", "âm nhạc", "sách truyện", "áp lực", "thi cử"]
    return render_template('cold_start.html', user_id = id, tags=tags, list_tags=list_tags)

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
    bookmarks = BookMarks.query.order_by(BookMarks.date_posted)
    return render_template('dashboard.html', user=user, all_blogs=all_blogs, bookmarks=bookmarks)

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
    
# ----------- Tags management -----------
@app.route("/tags", methods=["GET", "POST"]) 
def tags():
    taglist = request.form.getlist('tags[]') 
    return render_template("tags.html", taglist=taglist)
    
    
# ----------- Blog management -----------
@app.route("/create_blog", methods=["GET", "POST"]) 
@login_required
def create_blog():
    title = None
    form = PostBlogForm()
    if form.validate_on_submit():
        poster = current_user.id
        title = form.title.data
        post = Blogs(title=form.title.data,
                     poster_id = poster,
                     content=form.content.data,
                     )
        db.session.add(post)
        db.session.commit()
        
        
        title = form.title.data
        form.title.data = ''
        form.content.data = ''
        
        # tags processing
        tag_list = request.form.getlist('tags[]') 
        str_tag = encoding(tag_list)
        blog = Blogs.query.filter_by(poster_id=poster, title=title).first()
        tag = Tags(blog_id = blog.id, content=str_tag)
        db.session.add(tag)
        db.session.commit()
        print(tag_list)
        
        util_matrix.init_or_update_csv(Users_query=Users.query.count(), Blogs_query=Blogs.query.count())
        return redirect(url_for('dashboard', id=current_user.id))
              
    return render_template("create_blog.html", title=title, form=form)

def encoding(tag_list):
    return '/'.join(tag_list)

def decoding(str_list):
    return str_list.split('/')

def blog_id_bookmark(blogid):
    # Bookmarks
    temp2 = None
    bookmarks =  BookMarks.query.order_by(BookMarks.date_posted)
    for bookmark in bookmarks:
        if bookmark.bookmarker.id == current_user.id and bookmark.blog_id == blogid:
            temp2 = bookmark.bookmark_state
            
    return temp2


    

@app.route("/all_blogs")
def all_blogs():
    all_blogs = Blogs.query.order_by(Blogs.date_posted)    
    
    # Bookmarks
    bookmarks =  BookMarks.query.order_by(BookMarks.date_posted)
    tags = Tags.query.order_by(Tags.date_posted)
    list_tags = ["cảm xúc", "chủng tộc", "sở thích", "du lịch", "thể thao", "hẹn hò", "gia đình", "đồng nghiệp", "bạn bè", "tâm lý", "nhân cách", "âm nhạc", "sách truyện", "áp lực", "thi cử"]
    categories = Categories.query.order_by(Categories.date_posted)
    
    img_categories = ['rm_2.png', 'rm_3.png', 'rm_4.png', 'rm_5.png', 'rm_6.png'] 
    
    return render_template("all_blogs.html", all_blogs=all_blogs, bookmarks=bookmarks, blog_id_bookmark=blog_id_bookmark, tags=tags, decoding=decoding, list_tags=list_tags, categories=categories, img_categories=img_categories, zip=zip)

@app.route("/all_blogs_filter/<string:query>")
def all_blogs_filter(query):
    all_blogs = Blogs.query.order_by(Blogs.date_posted)    
    print(query)
    
    # Bookmarks
    bookmarks =  BookMarks.query.order_by(BookMarks.date_posted)
    tags = Tags.query.order_by(Tags.date_posted)
    list_tags = ["cảm xúc", "chủng tộc", "sở thích", "du lịch", "thể thao", "hẹn hò", "gia đình", "đồng nghiệp", "bạn bè", "tâm lý", "nhân cách", "âm nhạc", "sách truyện", "áp lực", "thi cử"]
    
    return render_template("all_blogs_filter.html", all_blogs=all_blogs, bookmarks=bookmarks, blog_id_bookmark=blog_id_bookmark, tags=tags, decoding=decoding, list_tags=list_tags, query=query)



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

@app.route("/reactions", methods=["GET", "POST"])
def reactions():
    emotion = request.form['emotion'] 
    blogid = request.form['id']            
    reactions = Reactions.query.order_by(Reactions.date_posted)
    reacted = False # flag variable to indicate whether the user has already reacted
    for reaction in reactions:
        # if user already reacts -> update reaction in database
        if reaction.reacter.id == current_user.id and reaction.blog_id == int(blogid):
            reaction_data = Reactions.query.get_or_404(reaction.id)
            reaction_data.reaction_type = emotion
            db.session.add(reaction_data)
            db.session.commit()
            reacted = True # set the flag to True
            break 
    # if user has not reacted -> add new to database 
    if not reacted:
        reaction = Reactions(reaction_type=emotion, reacter_id=current_user.id, blog_id=blogid)
        db.session.add(reaction)
        db.session.commit()
                    
    return redirect(url_for('blog', id=blogid))

@app.route("/bookmark", methods=["GET", "POST"])
def bookmark():
    if request.method == "POST":
        blogid = request.form.get("id")
        bookmarked_state = request.form.get("bookmark_state") 
        if bookmarked_state == "true":
            # Add to the database
            bookmark = BookMarks(bookmark_state=bookmarked_state, bookmarker_id=current_user.id, blog_id=blogid)
            db.session.add(bookmark)
            db.session.commit()
        else:
            # find the existing bookmark object and delete it from the database
            bookmark = BookMarks.query.filter_by(bookmarker_id=current_user.id, blog_id=blogid).first()
            db.session.delete(bookmark)
            db.session.commit()

        return redirect(url_for('blog', id=blogid))
    
@app.route("/bookmark2", methods=["GET", "POST"])
def bookmark2():
    if request.method == "POST":
        blogid = request.form.get("id")
        bookmarked_state = request.form.get("bookmark_state") 
        bookmark_id = request.form.get("bookmark_id") 
        
        if bookmarked_state == "true":
            # Add to the database
            bookmark = BookMarks(bookmark_state=bookmarked_state, bookmarker_id=current_user.id, blog_id=blogid)
            db.session.add(bookmark)
            db.session.commit()
        else:
            # find the existing bookmark object and delete it from the database
            bookmark = BookMarks.query.filter_by(bookmarker_id=current_user.id, blog_id=blogid).first()
            db.session.delete(bookmark)
            db.session.commit()
 
        return redirect(url_for('all_blogs'))
        


import time
@app.route("/blog/<int:id>", methods=["GET", "POST"])
def blog(id):
    blog = Blogs.query.get_or_404(id)
    # Comments
    commentForm = CommentForm()
    if commentForm.validate_on_submit():
        comment = Comments(blog_id=blog.id,
                        commenter_id = current_user.id,
                        comment_content=commentForm.content.data,
                        )
        db.session.add(comment)
        db.session.commit()
        
        commentForm.content.data = ''
    all_comments = Comments.query.order_by(Comments.date_posted)
    
    # Reactions
    temp = None
    reactions = Reactions.query.order_by(Reactions.date_posted)
    for reaction in reactions:
        if reaction.reacter.id == current_user.id and reaction.blog_id == id:
            temp = reaction.reaction_type
            
    # Bookmarks
    temp2 = None
    bookmarks =  BookMarks.query.order_by(BookMarks.date_posted)
    for bookmark in bookmarks:
        if bookmark.bookmarker.id == current_user.id and bookmark.blog_id == id:
            temp2 = bookmark.bookmark_state
    
    start_time = datetime.utcnow()
    start_time_str = start_time.strftime("%H:%M:%S")
    start_time_sec = convert_to_sec(start_time_str)
    return render_template('blog.html', blog=blog, start_time_sec=start_time_sec, datetime=datetime, commentForm=commentForm, all_comments=all_comments, reactions=reactions, bookmarks=bookmarks, temp=temp, temp2=temp2)

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

@app.route("/edit_podcast")
def edit_podcast():
    podcast = Audio.query.get_or_404(1)
    podcast.title = "Bài học trưởng thành"
    db.session.add(podcast)
    db.session.commit()
    return redirect(url_for('all_podcasts'))
    
 

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
    