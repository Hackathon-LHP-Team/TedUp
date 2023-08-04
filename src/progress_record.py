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
tab1, tab2, tab3 = st.tabs(["Detailed Analysis", "Analysis for user", "Detailed Dataframe"])


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
    Chat_need_process = df.iloc[:,(len(df.columns) - 1)].tolist()
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

with tab1:
    # developer()
    user()
    # pass
    
    
with tab2:
    st.subheader("Overall Analysis - Q value")
    Q = pd.read_csv('assets/Q_value.csv')
    fig = px.line(Q, x=Q.index, y=Q.columns)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Detailed Analysis - S value")
    s_res_list = pd.read_csv('assets/s_res_list.csv')
    fig = px.line(s_res_list, x=s_res_list.index, y=s_res_list.columns)
    st.plotly_chart(fig, use_container_width=True)
    
    # barchart()
    barchart_2()
    
with tab3:
    df = pd.read_csv('assets/Emotion_assessment.csv')
    st.dataframe(df, use_container_width=True)