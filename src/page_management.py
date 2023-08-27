import streamlit as st
from st_pages import Page, show_pages, add_page_title

def management():
    show_pages(
        [
            Page("home.py", "Home"),
            Page("app.py", "Authentication"),
            Page("main.py", "App"),
            Page("progress_record.py", "Progress Record"),
        ]
    )