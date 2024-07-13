import streamlit as st  
import requests
import json

def add_department(data):
    
    data_j = json.loads(data.json())
    data_j['created_at'] = None
    data_j['updated_at'] = None

    try:
      return requests.post(st.session_state.api_url + '/department', json=data_j)
    except requests.exceptions.RequestException as e:
      return e

def get_departments():  
    try:
      return requests.get(st.session_state.api_url + '/departments')
    except requests.exceptions.RequestException as e:
      return e

def update_department(data):
      
      data_j = json.loads(data.to_json())
      data_j['created_at'] = None
      data_j['updated_at'] = None
      id = data_j['id']
      data_j.pop('id')
  
      try:
        return requests.put(st.session_state.api_url + '/department/' + str(id), json=data_j)
      except requests.exceptions.RequestException as e:
        return e