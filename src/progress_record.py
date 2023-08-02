# streamlit components
import streamlit as st
# from streamlit_option_menu import option_menu
from page_setup_config import page_configure

# machine learning libs
import numpy as np


# set up page configuration
page_configure()

# define the on_change function
# def on_change(key):
#     selection = st.session_state[key]
#     if selection == "Home":
#         st.write("home")

# # create the option menu
# selected5 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'],
#                         icons=['house', 'cloud-upload', "list-task", 'gear'],
#                         on_change=on_change, key='menu_5', orientation="horizontal",
#                         styles={
#                             "nav-link-selected": {"background-color": "black"},
#                         })



tab1, tab2 = st.tabs(["Chart", "Data"])
data = np.random.randn(10, 1)

tab1.subheader("Progress History Record")
tab1.line_chart(data)

tab2.subheader("Data Record")
tab2.write(data)



