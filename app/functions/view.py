import os
from dotenv import load_dotenv


def get_width(st, stj):
    while 'wide_mode' not in st.session_state:
        try:
            st.session_state.viewport_width = stj(
                js_expressions='window.innerWidth', key='ViewportWidth'
            )

            if st.session_state.viewport_width < 600:
                st.session_state.wide_mode = 'wide'
            else:
                st.session_state.wide_mode = 'centered'
        except:
            pass


def back_to_menu(st):
    st.subheader('')
    if st.button('Voltar Para o Início'):
        st.switch_page('pages/select_step.py')


def hide_menu(st):
    st.markdown(
        """
      <style>
          .reportview-container {
              margin-top: -2em;
          }
          #MainMenu {visibility: hidden;}
          .stDeployButton {display:none;}
          footer {visibility: hidden;}
          #stDecoration {display:none;}
      </style>
  """,
        unsafe_allow_html=True,
    )


def redirect_with(st):
    if 'wide_mode' not in st.session_state:
        st.switch_page('app.py')
    if 'api_url' not in st.session_state:
        st.session_state.api_url = os.getenv('API_URL')
