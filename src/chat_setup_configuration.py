import streamlit as st


def page_configure():
    st.set_page_config(
        page_title="Virtual Therapist",
        page_icon="🧊",
        initial_sidebar_state="collapsed",
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# This is a header. This is an *extremely* cool app!"
        }
    )