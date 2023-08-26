import streamlit as st

def customization():

    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url(https://cdn.glitch.global/0b0c1622-4f23-4acc-8587-e456a037e413/bg_final.png?v=1693041587015);
        background-size: cover;
        background-position: top left;
        background-repeat: no-repeat;
        background-attachment: local;
        background-attachment: fixed;
    }}


    [data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0);
    }}
    
    [data-testid="stSidebar"] > div:first-child {{
        background-color: rgba(0,0,0,0);
    }}

    /* Added this part to remove the solid background around the chat input */
    .css-usj922 {{
        background-color: transparent;
    }}

    </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)
