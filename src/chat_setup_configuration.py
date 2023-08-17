import streamlit as st

def page_configure():
    st.set_page_config(
        page_title="Virtual Therapist",
        page_icon="https://cdn.glitch.global/0b0c1622-4f23-4acc-8587-e456a037e413/favicon.png?v=1691305859804",
        initial_sidebar_state="collapsed",
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# This is a header. This is an *extremely* cool app!"
        }
    )