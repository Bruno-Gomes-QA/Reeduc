import streamlit as st
import requests
import json

def get_peoples_types():  
  try:
    return requests.get(st.session_state.api_url + '/peopletypes')
  except requests.exceptions.RequestException as e:
    return e
  
def get_peoples():  
  try:
    return requests.get(st.session_state.api_url + '/peoples')
  except requests.exceptions.RequestException as e:
    return e
