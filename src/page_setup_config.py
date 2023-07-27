import streamlit as st
from st_pages import Page, show_pages, add_page_title

def page_configure():
    st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    initial_sidebar_state="expanded",
    layout="wide",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)