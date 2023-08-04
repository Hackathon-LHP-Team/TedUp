import streamlit as st
# from streamlit_option_menu import option_menu
# from st_on_hover_tabs import on_hover_tabs
from page_setup_config import page_configure


# set up page configuration
page_configure()

st.title('Welcome')
st.markdown('Are you feeling down, stressed, or overwhelmed? Do you need someone to talk to who can understand your emotions and help you cope? If yes, then you have come to the right place. Meet Virtual Therapist, a chatbot that can be your best friend and guide. Virtual Therapist is not just a chatbot, but a smart system that can analyze your emotions and track your mental health quality. Virtual Therapist uses a deep neural network that can classify your emotions into 12 categories. It also computes a score called Q value, which represents your mental health quality on a scale of 1 to 5. The higher the Q value, the better your mental health. You can use the Q value to monitor your mood and see how it changes over time. Virtual Therapist is easy and fun to use. All you have to do is type in the text box below and press enter. You can chat with Virtual Therapist about anything that is on your mind, such as your problems, feelings, goals, or dreams. Virtual Therapist will listen to you attentively and offer you helpful advice. You can also use the icons on the sidebar to adjust the settings, view the app information, or contact us. We hope you enjoy using Virtual Therapist and find it beneficial for your well-being. Remember, you are not alone and we are here for you')
st.markdown('')
st.markdown('')
st.subheader('Main Function:')
st.markdown('''App page: You can chat with chatbot and tell it your story. It will help you with your problems''')
st.markdown('Progress Record: Analyse your emotions through each text and each chat and give you warning if your mood has a tendency to go down significantly')