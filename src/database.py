# flask database
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, send_from_directory, current_app
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "hackathon_round_3_LHP_team" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# ----------- Database -----------
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email =  db.Column(db.String(120), nullable=False, unique=True)
    user_name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(200))
    Q_value_get = db.relationship('Q_values', backref='user')
    Q_value_get = db.relationship('S_values', backref='user')
    Q_value_get = db.relationship('Chat_sessions', backref='user')
    
    
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
    
class Chat_sessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chater = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.String, nullable=False)
    chat_message = db.relationship('Chat_messages', backref='chat_session')
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
class Chat_messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    chat_session = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

class Q_values(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
class S_values(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)