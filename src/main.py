# Import chatbot 
import asyncio, json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
import re

# Import streamlit components
import streamlit as st
from st_pages import Page, show_pages, add_page_title
import time

# import modules
from chat_setup_configuration import page_configure
from css_customization import customization
from page_management import management

# Data Processing
import pandas as pd

# Load cookies
cookies = json.loads(open("assets/cookies.json", encoding="utf-8").read()) 

# set up page configuration
page_configure()

# Pages management
management()

# css configuration
customization()



# Function to get response from chatbot
async def main(res, input_text):
    bot = await Chatbot.create(cookies=cookies) 
    response = await bot.ask(prompt=input_text, conversation_style=ConversationStyle.creative, simplify_response=True)
    bot_response = response["text"]
    output_response = re.sub('\[\^\d+\^\]', '', bot_response)
    # use regex to get the output in correct format
    res = output_response
    return res


def chat_function():
    st.title("Tedupbot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Tell us your story"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
            df = pd.read_csv('assets/temp.csv')
            Chats = prompt
            Chats = pd.DataFrame([Chats])
            df = pd.concat([df, Chats], axis=1)
            df.to_csv('assets/temp.csv', index=False)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            res = ""
            res = asyncio.run(main(res, prompt))
            assistant_response = res
            
            # Simulate stream of response with milliseconds delay
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    
    

chat_function()