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
    S_value_get = db.relationship('S_values', backref='user')
    chat_session_get = db.relationship('Chat_sessions', backref='user')
    
    
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.String, nullable=False)
    chat_message = db.relationship('Chat_messages', backref='chat_session')
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
class Chat_messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_sessions.id'))
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

# streamlit components
import streamlit as st

# from streamlit_option_menu import option_menu
from page_setup_config import page_configure

# visualization
import plotly.express as px

# machine learning libs
import pandas as pd
import numpy as np
from score import score

# set up page configuration
page_configure()
st.title('Progress Record and Mental Health Assessment')
tab1, tab2, tab3 = st.tabs(["Detailed Analysis", "Line Chart Anlysis", "BarChart and Message"])

# deep translation
from deep_trans import translate


# This function is used when developer want to quickly get a big database
# when using model to predict for all chats. This function can be used to quickly
# observe how the system work with prepared data 

def developer():
    Q = []
    s_res_list = []
    texts = []

    df = pd.read_csv('assets/Chats.csv')
    for i in range(len(df.columns)):
        st.subheader(f'Chat: {i + 1}')
        Chats = df.iloc[:,i].tolist()
        st.write(Chats)
        texts.extend(Chats[1:])
        
        # Call class to do analysis (see example in test.py)
        Chats = translate(Chats)
        score_obj = score(Chats)
        tokenizer = score_obj.generate_token()
        padded_chat_seq = score_obj.tokenize_text(tokenizer)
        Q_res, s_res = score_obj.Q_value(padded_chat_seq)

        s_res = s_res[1:]
        s_res_list.extend(s_res)
        st.write(s_res)
        Q.append(Q_res)

        s_res = pd.DataFrame(s_res)
        fig = px.line(s_res, x=s_res.index, y=s_res.columns)
        st.plotly_chart(fig, use_container_width=True)
    
    
    df = pd.DataFrame(data={"Your Chat Text": texts, "Emotion Assessment Score": s_res_list})
    df.to_csv('assets/Emotion_assessment.csv', index=False) 
    
    Q = pd.DataFrame(Q)
    Q.to_csv('assets/Q_value.csv', index=False)
    
    s_res_list = pd.DataFrame(s_res_list)
    s_res_list.to_csv('assets/s_res_list.csv', index=False)


# This function is used when product being deployed for usage.
# The database will be automatically updated when new chat appears (user chat with chat bot)
# This function only compute the latest chat and update it to the database

def user():
    st.subheader('Chat history')
    df = pd.read_csv('assets/Chats.csv')
    st.dataframe(df, use_container_width=True)
    Chat_need_process = df.iloc[:,24].tolist()
    st.write(Chat_need_process)
    
    st.subheader('Assessment on new chat')
    
    # Call class to do analysis (see example in test.py)
    score_obj = score(Chat_need_process)
    tokenizer = score_obj.generate_token()
    padded_chat_seq = score_obj.tokenize_text(tokenizer)
    Q_res, s_res = score_obj.Q_value(padded_chat_seq)
    
    Q_value = pd.read_csv("assets/Q_value.csv")
    Q_value = Q_value.iloc[:,0].values.tolist()
    Q_value.append(Q_res)
    Q_value = pd.DataFrame(Q_value)
    Q_value.to_csv('assets/Q_value.csv', index=False)
    
    s_res = s_res[1:]
    st.write("S Value")
    st.write(s_res)
    st.write("Q Value")
    st.write(Q_res)
    
    s_res_list = pd.read_csv('assets/s_res_list.csv')
    s_res_list = s_res_list.T
    s_res_list.to_csv('assets/s_res_list.csv', index=False)
    s_res_list = pd.read_csv('assets/s_res_list.csv')
    
    s_res = pd.DataFrame(s_res)
    s_res = s_res.T
    s_res_list = pd.concat([s_res_list, s_res], axis=1, ignore_index=True)
    s_res_list = s_res_list.T
    s_res_list.to_csv('assets/s_res_list.csv', index=False)  
    
    
    df_emotion_assessment = pd.read_csv('assets/Emotion_assessment.csv')
    User_chat_text = df_emotion_assessment.iloc[:,0].values.tolist()
    User_chat_text.extend(Chat_need_process[1:])
    
    s_res_list = pd.read_csv('assets/s_res_list.csv')
    s_res_list = s_res_list.iloc[:,0].values.tolist()

    df_emotion_assessment = pd.DataFrame(data={"Your Chat Text": User_chat_text, "Emotion Assessment Score": s_res_list})
    df_emotion_assessment.to_csv('assets/Emotion_assessment.csv', index=False)
    
    

# Developer mode
def barchart():
    list_emotions = []
    df = pd.read_csv('assets/Chats.csv')
    for i in range(len(df.columns)):
        Chats = df.iloc[:,i].values.tolist()
        
        score_obj = score(Chats[1:])
        tokenizer = score_obj.generate_token()
        padded_chats_seq = score_obj.tokenize_text(tokenizer)
        
        for chat in padded_chats_seq:
            list_emotions.append(score_obj.predict2([chat.tolist()]))
    
    list_emotions = pd.DataFrame(list_emotions)
    list_emotions.to_csv('assets/list_emotions.csv', index=False)
    fig = px.histogram(list_emotions, color=list_emotions.iloc[:,0])
    st.plotly_chart(fig, use_container_width=True)
    st.success("You have positive emotions more frequently than negative emotions. It's awesome. Wish you keep this progress.")
    

# User mode
def barchart_2():
    df = pd.read_csv('assets/Chats.csv')
    Chat_need_process = df.iloc[:,(len(df.columns) - 1)].values.tolist()
    
    # Call class to do analysis (see example in test.py)
    score_obj = score(Chat_need_process[1:])
    tokenizer = score_obj.generate_token()
    padded_chat_seq = score_obj.tokenize_text(tokenizer)
    
    list_emotion = []
    for chat in padded_chat_seq:
        list_emotion.append(score_obj.predict2([chat.tolist()]))
        
    list_emotions = pd.read_csv("assets/list_emotions.csv").iloc[:,0].tolist()
    list_emotions.extend(list_emotion)
    
    list_emotions = pd.DataFrame(list_emotions)
    fig = px.histogram(list_emotions, color=list_emotions.iloc[:,0])
    st.plotly_chart(fig, use_container_width=True)
    list_emotions.to_csv('assets/list_emotions.csv', index=False)
    
    num_positive = len(df[df == 'Positive Emotions'])
    num_negative = len(df[df == 'Negative Emotions'])
    
    if num_negative < num_positive:
        st.success("You have positive emotions more frequently than negative emotions. It's awesome. Wish you keep this progress.")
    else:
        st.warning("You have negative emotions more frequently than positive emotions. It's not good. If this trend continues, we will send this case to emergency service.")
         
        
def database_analysis():
    with app.app_context():
        all_sessions = Chat_sessions.query.order_by(Chat_sessions.date_posted)
        
        Q_value = []
        s_res_list = []
        for session in all_sessions:
            st.subheader(f"Session: {session.content}")
            list_session = []
            st.write(session.content)
            all_messages = Chat_messages.query.order_by(Chat_messages.date_posted)
            for message in all_messages:
                if message.session_id == session.id:
                    st.write(message.content)
                    list_session.append(message.content)
                    
            list_session = translate(list_session)
            score_obj = score(list_session)
            tokenizer = score_obj.generate_token()
            padded_chat_seq = score_obj.tokenize_text(tokenizer)
            Q_res, s_res = score_obj.Q_value(padded_chat_seq)
            
            st.write(s_res)
            st.write(Q_res)
            
            Q_value.append(Q_res)
            s_res_list.extend(s_res)
            

        Q_value = pd.DataFrame(Q_value)
        s_res_list = pd.DataFrame(s_res_list)
        Q_value.to_csv('assets/Q_value.csv', index=False)
        s_res_list.to_csv('assets/s_res_list.csv', index=False)
        
                    

with tab1:
    database_analysis()
    
with tab2:
    st.subheader("Overall Analysis - Q value")
    Q = pd.read_csv('assets/Q_value.csv')
    fig = px.line(Q, x=Q.index, y=Q.columns)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Detailed Analysis - S value")
    s_res_list = pd.read_csv('assets/s_res_list.csv')
    fig = px.line(s_res_list, x=s_res_list.index, y=s_res_list.columns)
    st.plotly_chart(fig, use_container_width=True)
    
    
    
with tab3:
    list_emotions = pd.read_csv('assets/list_emotions.csv')
    fig = px.histogram(list_emotions, color=list_emotions.iloc[:,0])
    st.plotly_chart(fig, use_container_width=True)
    st.warning("Tình trạng chất lượng cảm xúc và sức khỏe tâm thần của bạn đang không được tốt với số cảm xúc tiêu cực cao hơn nhiều so với cảm xúc tích cực. Nếu tình trạng này kéo dài và có dấu hiệu đi xuống, chúng tôi sẽ giúp bạn có giải pháp giải quyêt kịp thời")
    