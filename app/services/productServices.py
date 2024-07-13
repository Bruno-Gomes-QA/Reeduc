import streamlit as st
import requests
import json

def add_product(data):
    
    data_j = json.loads(data.json())
    data_j['department_id'] = int(data_j['department_id'][0])
    data_j['created_at'] = None
    data_j['updated_at'] = None
    print(data_j)
    try:
      return requests.post(st.session_state.api_url + '/product', json=data_j)
    except requests.exceptions.RequestException as e:
      return e

def get_products():  
  try:
    return requests.get(st.session_state.api_url + '/products')
  except requests.exceptions.RequestException as e:
    return e

def update_product(data, id):
      

      data_j = json.loads(data.to_json())
      data_j['created_at'] = None
      data_j['updated_at'] = None
  
      try:
        return requests.put(st.session_state.api_url + '/product/' + str(id), json=data_j)
      except requests.exceptions.RequestException as e:
        return e