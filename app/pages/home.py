import streamlit as st
from functions import hide_menu, redirect_with
import pandas as pd
import numpy as np

st.set_page_config(page_title='Início', layout='wide')

hide_menu(st)
redirect_with(st)

st.title('Reciclagem Primícias ♻️', anchor=False)
st.subheader('')

col1, col2, col3, col4 = st.columns(4)

st.write('')

chart_data = pd.DataFrame(np.random.randn(10, 3), columns=["a", "b", "c"])
with col1:
    container1 = col1.container(border=True)
    container1.write('Produtos mais Comprados')
    container1.bar_chart(chart_data)
    if st.button('Produtos'):
        st.switch_page('pages/products.py')
with col2:
    container2 = col2.container(border=True)
    container2.write('Departamentos mais Vendidos')
    container2.line_chart(chart_data)
    if st.button('Departamentos'):
        st.switch_page('pages/departments.py')
with col3:
    container3 = col3.container(border=True)
    container3.write('Top Fornecedores')
    container3.bar_chart(chart_data)
    if st.button('Fornecedores'):
        st.switch_page('pages/peoples.py')
with col4:
    container4 = col4.container(border=True)
    container4.write('Compra Semanal')
    container4.line_chart(chart_data)
    if st.button('Compras'):
        st.switch_page('pages/purchases.py')