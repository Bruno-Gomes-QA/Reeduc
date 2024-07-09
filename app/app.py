import os
from dotenv import load_dotenv
import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from functions import get_width, hide_menu

load_dotenv()

st.set_page_config(page_title='Home', layout='centered')
get_width(st, streamlit_js_eval)
hide_menu(st)

if 'api_url' not in st.session_state:
    st.session_state.api_url = os.getenv('API_URL')

st.switch_page('pages/home.py')
