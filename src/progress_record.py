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
        
        # Create an object of the class
        score_obj = score(Chats)

        # Call the methods on the object
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


def user():
    df = pd.read_csv('assets/Chats.csv')
    st.dataframe(df, use_container_width=True)
    Chat_need_process = df.iloc[:,(len(df.columns) - 1)].tolist()
    st.write(Chat_need_process)
    
    # Create an object of the class
    score_obj = score(Chat_need_process)

    # Call the methods on the object
    tokenizer = score_obj.generate_token()
    padded_chat_seq = score_obj.tokenize_text(tokenizer)
    Q_res, s_res = score_obj.Q_value(padded_chat_seq)
    
    # s_res = s_res[1:]
    # st.write(s_res)
    
    # s_res_list = pd.read_csv('assets/s_res_list.csv')
    # s_res_list = s_res_list.T
    # s_res_list.to_csv('assets/s_res_list.csv', index=False)
    # s_res_list = pd.read_csv('assets/s_res_list.csv')
    # st.write(s_res_list)
    
    # s_res = pd.DataFrame(s_res)
    # s_res = s_res.T
    # s_res_list = pd.concat([s_res_list, s_res], axis=1, ignore_index=True)
    # s_res_list = s_res_list.T
    # print(s_res_list)
    # st.write(s_res_list)
    # s_res_list.to_csv('assets/s_res_list.csv', index=False)   
    
def user2():
    pass


with tab1:
    # developer()
    # user()
    pass
    
    
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
    df = pd.read_csv('assets/Emotion_assessment.csv')
    st.dataframe(df, use_container_width=True)