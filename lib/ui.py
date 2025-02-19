import streamlit as st
from datetime import datetime
import os
from .form_data import QAFormData
from .pdf_generator import PDFGenerator
from .styles import get_css
from .translations import set_language, _

def initialize_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 1
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    if 'language' not in st.session_state:
        st.session_state.language = 'pt_BR'
    if 'should_update_language' not in st.session_state:
        st.session_state.should_update_language = False
        set_language('pt_BR')

def on_language_change():
    new_lang = st.session_state.language_selector
    if new_lang != st.session_state.language:
        st.session_state.language = new_lang
        st.session_state.should_update_language = True

class QAFormUI:
    def __init__(self):
        self.form_data = QAFormData()
        initialize_session_state()
        
        st.markdown(get_css(), unsafe_allow_html=True)
        self.reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)

    def render(self):
        if st.session_state.should_update_language:
            set_language(st.session_state.language)
            st.session_state.should_update_language = False
            st.rerun()
            
        self._render_language_selector()
        self._render_header()
        
        if st.session_state.page == 1:
            self._render_basic_info()
        elif st.session_state.page == 2:
            self._render_ux_ui()
        elif st.session_state.page == 3:
            self._render_functionality()
        elif st.session_state.page == 4:
            self._render_code_quality()
        elif st.session_state.page == 5:
            self._render_extra_validations()
        elif st.session_state.page == 6:
            self._render_feedback()
        elif st.session_state.page == 7:
            self._render_success()

    def _render_language_selector(self):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col3:
            language_options = {
                'pt_BR': 'Português (Brasil)',
                'en_US': 'English (US)'
            }
            st.selectbox(
                _("Language/Idioma"),
                options=list(language_options.keys()),
                format_func=lambda x: language_options[x],
                index=0 if st.session_state.language == 'pt_BR' else 1,
                key='language_selector',
                on_change=on_language_change
            )

    def _render_header(self):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.title(_("Formulário de Validação QA"))
        with col2:
            st.progress(st.session_state.page/7, _("Etapa {}/7").format(st.session_state.page))

    def _collect_basic_info(self):
        st.session_state.form_data['data_avaliacao'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        st.session_state.form_data['nome_avaliador'] = st.text_input(_("Nome do Avaliador"), placeholder=_("Nome do avaliador"))
        st.session_state.form_data['nome_engenheiro'] = st.text_input(_("Nome do Engenheiro"), placeholder=_("Nome do engenheiro responsável pela entrega"))
        st.session_state.form_data['funcionalidade'] = st.text_input(_("Funcionalidade/Entrega"), placeholder=_("Qual funcionalidade ou entrega foi validada?"))
        st.session_state.form_data['versao'] = st.text_input(_("Versão do Produto"), placeholder=_("Versão do produto no pacote ou do release a ser lançado"))
        st.session_state.form_data['id_tarefa'] = st.text_input(_("Identificação da Tarefa"), placeholder=_("ID da Tarefa"))

    def _validate_basic_info(self):
        return all([
            st.session_state.form_data.get('nome_avaliador'),
            st.session_state.form_data.get('nome_engenheiro'),
            st.session_state.form_data.get('funcionalidade'),
            st.session_state.form_data.get('versao'),
            st.session_state.form_data.get('id_tarefa')
        ])

    def _render_basic_info(self):
        st.header(_("Informações Básicas"))
        with st.form("info_basica"):
            self._collect_basic_info()
            if st.form_submit_button(_("Próximo")):
                if self._validate_basic_info():
                    st.session_state.page = 2
                else:
                    st.error(_("Por favor, preencha todos os campos!")) 