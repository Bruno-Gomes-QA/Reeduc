import streamlit as st
from functions import hide_menu, redirect_with
import streamlit_pydantic as sp
from services import productServices as ps
from services import departmentServices as ds
import pandas as pd
from time import sleep


st.set_page_config(page_title='Produtos', layout='wide')

hide_menu(st)
redirect_with(st)

if st.button('Voltar'):
    st.switch_page('pages/home.py')
st.subheader('')

col1, col2 = st.columns(2)

departments = ds.get_departments()
if departments.json()['data'] == []:
    st.write('')
    st.write('Nenhum departamento cadastrado, por favor cadastre um departamento antes de criar um produto.')
    if st.button('Cadastrar Departamento'):
        st.switch_page('pages/departments.py')
else:
    with col1:
        from models import ProductModel
        st.subheader('Cadastro de Produtos')
        data = sp.pydantic_form(key="my_form", model=ProductModel, submit_label='Criar Produto', clear_on_submit=True)
    if data:
        if data.product_name != '' or data.product_description != '':
            response = ps.add_product(data)
            if response.status_code == 201:
                col1.success('Produto criado com sucessos')
            else:
                col1.error('Erro ao criar produto')
        else:
            col1.error('Preencha os campos obrigatórios')
            sleep(0.5)
            col1.rerun()
    products = ps.get_products()
    if products.json()['data'] == []:
        col2.subheader('')
        col2.warning('Nenhum produto cadastrado')
    else:
        col2.subheader('Produtos')
        col2.write('Aqui estão todos os produtos cadastrados, para editar altere o valor na tabela abaixo e clique em Atualizar Produtos')
        col2.write('')

        df = pd.DataFrame(products.json()['data'], columns=['id', 'product_name', 'product_description', 'buy_price', 'sale_price', 'stock'])
        edited_df = col2.data_editor(df, column_config={  'id': {'editable': False, 'label': 'ID', 'disabled': True},
                                                        'product_name': {'editable': True, 'label': 'Nome'},
                                                        'product_description': {'editable': True, 'label': 'Descrição'},
                                                        'buy_price': {'editable': True, 'label': 'Preço de Compra'},
                                                        'sale_price': {'editable': True, 'label': 'Preço de Venda'},
                                                        'stock': {'editable': True, 'label': 'Estoque'}
                                                    },
                                use_container_width=True,
                                hide_index=True
                                    )

        if col2.button('Atualizar Produtos'):
            with col2.status("Atualizando Produtos..."):
                update = False
                for index, row in edited_df.iterrows():
                    if not row.equals(df.iloc[index]):
                        update = True
                        response = ps.update_product(row, index+1)
                        if response.status_code == 200:
                            col2.toast(f"Produto {row['name']} atualizado com sucesso")
                        else:
                            col2.error('Erro ao atualizar produto')
                if not update:
                    col2.toast('Nenhum produto foi alterado')
            sleep(2)
            col2.rerun()