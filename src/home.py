import streamlit as st
# from streamlit_option_menu import option_menu
# from st_on_hover_tabs import on_hover_tabs
from page_setup_config import page_configure


# set up page configuration
page_configure()

# define the on_change function
# def on_change(key):
#     selection = st.session_state[key]
#     pass

# # create the option menu
# selected5 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'],
#                         icons=['house', 'cloud-upload', "list-task", 'gear'],
#                         on_change=on_change, key='menu_5', orientation="horizontal",
#                         styles={
#                             "nav-link-selected": {"background-color": "black"},
#                         })




# st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)


# with st.sidebar:
#         tabs = on_hover_tabs(tabName=['Dashboard', 'Money', 'Economy'], 
#                              iconName=['dashboard', 'money', 'economy'],
#                              styles = {'navtab': {'background-color':'#111',
#                                                   'color': '#818181',
#                                                   'font-size': '14px',
#                                                   'font-family: georgia'
#                                                   'transition': '.3s',
#                                                   'white-space': 'nowrap',
#                                                   },
#                                        'tabOptionsStyle': {':hover :hover': {'color': '#241efb',
#                                                                       'cursor': 'pointer'}},
#                                        'iconStyle':{'position':'fixed',
#                                                     'left':'7.5px',
#                                                     'text-align': 'left'},
#                                        'tabStyle' : {'list-style-type': 'none',
#                                                      'margin-bottom': '30px',
#                                                      'padding-left': '30px'}},
#                              key="1")

# if tabs =='Dashboard':
#     st.title("Navigation Bar")
#     st.write('Name of option is {}'.format(tabs))

# elif tabs == 'Money':
#     st.title("Paper")
#     st.write('Name of option is {}'.format(tabs))

# elif tabs == 'Economy':
#     st.title("Tom")
#     st.write('Name of option is {}'.format(tabs))
