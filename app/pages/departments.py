import streamlit as st
from models import DepartmentModel
from functions import hide_menu, redirect_with
import streamlit_pydantic as sp
from services import departmentServices as ds
import pandas as pd
from time import sleep


st.set_page_config(page_title='Departamentos', layout='wide')

hide_menu(st)
redirect_with(st)

if st.button('Voltar'):
    st.switch_page('pages/home.py')
st.subheader('')

data = sp.pydantic_form(key="my_form", model=DepartmentModel, submit_label='Criar Departamento', clear_on_submit=True)
if data:
    if data.description == '' or data.name == '':
        st.error('Preencha todos os campos')
    else:
        response = ds.add_department(data)
        if response.status_code == 201:
            st.success('Departamento criado com sucesso')
            st.rerun()
        else:
            st.error('Erro ao criar departamento')

departments = ds.get_departments()
if departments.json()['data'] == []:
    st.write('')
    st.write('Nenhum departamento cadastrado')
else:
    st.subheader('Departamentos')
    st.write('Aqui estão todos os departamentos cadastrados, para editar altere o valor na tabela abaixo e clique em Atualizar Departamentos')
    st.write('')

    df = pd.DataFrame(departments.json()['data'], columns=['id', 'name', 'description', 'updated_at'])
    df['updated_at'] = pd.to_datetime(df['updated_at']).dt.strftime('%d/%m/%Y %H:%M:%S')
    edited_df = st.data_editor(df,
                            column_config={ 'id': {'editable': False, 'label': 'ID', 'disabled': True},
                                        'name': {'editable': True, 'label': 'Nome'},
                                        'description': {'editable': True, 'label': 'Descrição'},
                                        'updated_at': {'editable': False, 'label': 'Ultima Atualização', 'disabled': True}
                                        },
                            use_container_width=True,
                            hide_index=True
                               )

    if not edited_df.equals(df):
        if st.button('Atualizar Departamentos'):
            with st.status("Atualizando Departamentos..."):
                update = False
                for index, row in edited_df.iterrows():
                    if not row.equals(df.iloc[index]):
                        update = True
                        response = ds.update_department(row)
                        if response.status_code == 200:
                            st.toast(f"Departamento {row['name']} atualizado com sucesso")
                        else:
                            st.error('Erro ao atualizar departamento')
                if not update:
                    st.toast('Nenhum departamento foi alterado')
            sleep(2)
            st.rerun()