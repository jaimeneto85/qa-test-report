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
            if st.form_submit_button(_("Próximo"), type="primary"):
                if self._validate_basic_info():
                    st.session_state.page = 2
                else:
                    st.error(_("Por favor, preencha todos os campos!"))

    def _render_ux_ui(self):
        st.header(_("Conformidade com o Design UX/UI"))
        with st.form("ux_ui"):
            st.write(_("A entrega está 100% alinhada ao protótipo/UI design (Figma, Zeplin, etc)?"))
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                sim = st.checkbox(_("Sim"), key="ux_ui_alinhamento_sim")
            with col2:
                nao = st.checkbox(_("Não"), key="ux_ui_alinhamento_nao")
            with col3:
                st.session_state.form_data['ux_ui_alinhamento_obs'] = st.text_input(
                    _("Observações"),
                    key="obs_alinhamento",
                    label_visibility="collapsed"
                )
            
            if sim and nao:
                st.error(_("Por favor, selecione apenas Sim ou Não"))
            st.session_state.form_data['ux_ui_alinhamento'] = "Sim" if sim else "Não" if nao else None
            st.markdown("---")

            st.write(_("As cores, fontes, ícones e espaçamentos seguem o guia de estilo da empresa?"))
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                sim = st.checkbox(_("Sim"), key="ux_ui_guia_estilo_sim")
            with col2:
                nao = st.checkbox(_("Não"), key="ux_ui_guia_estilo_nao")
            with col3:
                st.session_state.form_data['ux_ui_guia_estilo_obs'] = st.text_input(
                    _("Observações"),
                    key="obs_guia_estilo",
                    label_visibility="collapsed"
                )
            st.session_state.form_data['ux_ui_guia_estilo'] = "Sim" if sim else "Não" if nao else None
            st.markdown("---")

            st.write(_("Componentes reutilizáveis e padrões de design foram respeitados?"))
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                sim = st.checkbox(_("Sim"), key="ux_ui_componentes_sim")
            with col2:
                nao = st.checkbox(_("Não"), key="ux_ui_componentes_nao")
            with col3:
                st.session_state.form_data['ux_ui_componentes_obs'] = st.text_input(
                    _("Observações"),
                    key="obs_componentes",
                    label_visibility="collapsed"
                )
            st.session_state.form_data['ux_ui_componentes'] = "Sim" if sim else "Não" if nao else None
            st.markdown("---")

            st.write(_("Experiência do usuário (UX) é fluida e sem pontos de atrito?"))
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                sim = st.checkbox(_("Sim"), key="ux_ui_experiencia_sim")
            with col2:
                nao = st.checkbox(_("Não"), key="ux_ui_experiencia_nao")
            with col3:
                st.session_state.form_data['ux_ui_experiencia_obs'] = st.text_input(
                    _("Observações"),
                    key="obs_experiencia",
                    label_visibility="collapsed"
                )
            st.session_state.form_data['ux_ui_experiencia'] = "Sim" if sim else "Não" if nao else None
            st.markdown("---")

            st.write(_("Transições, animações e interações estão implementadas conforme especificado?"))
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                sim = st.checkbox(_("Sim"), key="ux_ui_transicoes_sim")
            with col2:
                nao = st.checkbox(_("Não"), key="ux_ui_transicoes_nao")
            with col3:
                st.session_state.form_data['ux_ui_transicoes_obs'] = st.text_input(
                    _("Observações"),
                    key="obs_transicoes",
                    label_visibility="collapsed"
                )
            st.session_state.form_data['ux_ui_transicoes'] = "Sim" if sim else "Não" if nao else None

            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button(_("Anterior")):
                    st.session_state.page = 1
            with col2:
                if st.form_submit_button(_("Próximo"), type="primary"):
                    if st.session_state.form_data.get('ux_ui_alinhamento') is not None:
                        st.session_state.page = 3
                    else:
                        st.error(_("Por favor, responda se a entrega está alinhada ao protótipo!"))

    def _render_functionality(self):
        st.header(_("Funcionalidade e Comportamento"))
        with st.form("funcionalidade"):
            st.write(_("Todos os fluxos funcionam conforme esperado e especificado no UX?"))
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                sim = st.checkbox(_("Sim"), key="func_fluxos_sim")
            with col2:
                nao = st.checkbox(_("Não"), key="func_fluxos_nao")
            with col3:
                st.session_state.form_data['func_fluxos_obs'] = st.text_input(
                    _("Observações"),
                    key="obs_fluxos",
                    label_visibility="collapsed"
                )
            st.session_state.form_data['func_fluxos'] = "Sim" if sim else "Não" if nao else None
            st.markdown("---")

            st.write(_("Campos de formulário, botões e interações respondem corretamente?"))
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                sim = st.checkbox(_("Sim"), key="func_campos_sim")
            with col2:
                nao = st.checkbox(_("Não"), key="func_campos_nao")
            with col3:
                st.session_state.form_data['func_campos_obs'] = st.text_input(
                    _("Observações"),
                    key="obs_campos",
                    label_visibility="collapsed"
                )
            st.session_state.form_data['func_campos'] = "Sim" if sim else "Não" if nao else None
            st.markdown("---")

            st.write(_("Tratamento de erros e mensagens de validação estão implementados e alinhados ao design?"))
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                sim = st.checkbox(_("Sim"), key="func_erros_sim")
            with col2:
                nao = st.checkbox(_("Não"), key="func_erros_nao")
            with col3:
                st.session_state.form_data['func_erros_obs'] = st.text_input(
                    _("Observações"),
                    key="obs_erros",
                    label_visibility="collapsed"
                )
            st.session_state.form_data['func_erros'] = "Sim" if sim else "Não" if nao else None
            st.markdown("---")

            st.write(_("Comportamento responsivo (mobile, tablet, desktop) foi validado?"))
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                sim = st.checkbox(_("Sim"), key="func_responsivo_sim")
            with col2:
                nao = st.checkbox(_("Não"), key="func_responsivo_nao")
            with col3:
                st.session_state.form_data['func_responsivo_obs'] = st.text_input(
                    _("Observações"),
                    key="obs_responsivo",
                    label_visibility="collapsed"
                )
            st.session_state.form_data['func_responsivo'] = "Sim" if sim else "Não" if nao else None
            st.markdown("---")

            st.write(_("Funcionalidade foi testada em diferentes navegadores e sistemas operacionais?"))
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                sim = st.checkbox(_("Sim"), key="func_navegadores_sim")
            with col2:
                nao = st.checkbox(_("Não"), key="func_navegadores_nao")
            with col3:
                st.session_state.form_data['func_navegadores_obs'] = st.text_input(
                    _("Observações"),
                    key="obs_navegadores",
                    label_visibility="collapsed"
                )
            st.session_state.form_data['func_navegadores'] = "Sim" if sim else "Não" if nao else None

            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button(_("Anterior")):
                    st.session_state.page = 2
            with col2:
                if st.form_submit_button(_("Próximo"), type="primary"):
                    st.session_state.page = 4

    def _render_code_quality(self):
        st.header(_("Qualidade do Código e Testabilidade"))
        with st.form("qualidade_codigo"):
            st.write(_("Código segue os padrões internos e boas práticas de desenvolvimento?"))
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                sim = st.checkbox(_("Sim"), key="code_padroes_sim")
            with col2:
                nao = st.checkbox(_("Não"), key="code_padroes_nao")
            with col3:
                st.session_state.form_data['code_padroes_obs'] = st.text_input(
                    _("Observações"),
                    key="obs_padroes",
                    label_visibility="collapsed"
                )
            st.session_state.form_data['code_padroes'] = "Sim" if sim else "Não" if nao else None
            st.markdown("---")

            st.write(_("Há cobertura de testes unitários e de integração para as principais partes da funcionalidade?"))
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                sim = st.checkbox(_("Sim"), key="code_testes_sim")
            with col2:
                nao = st.checkbox(_("Não"), key="code_testes_nao")
            with col3:
                st.session_state.form_data['code_testes_obs'] = st.text_input(
                    _("Observações"),
                    key="obs_testes",
                    label_visibility="collapsed"
                )
            st.session_state.form_data['code_testes'] = "Sim" if sim else "Não" if nao else None
            st.markdown("---")

            st.write(_("Casos de teste automatizados foram implementados ou documentados?"))
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                sim = st.checkbox(_("Sim"), key="code_automatizados_sim")
            with col2:
                nao = st.checkbox(_("Não"), key="code_automatizados_nao")
            with col3:
                st.session_state.form_data['code_automatizados_obs'] = st.text_input(
                    _("Observações"),
                    key="obs_automatizados",
                    label_visibility="collapsed"
                )
            st.session_state.form_data['code_automatizados'] = "Sim" if sim else "Não" if nao else None
            st.markdown("---")

            st.write(_("A entrega está devidamente versionada e integrada com o repositório?"))
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                sim = st.checkbox(_("Sim"), key="code_versionamento_sim")
            with col2:
                nao = st.checkbox(_("Não"), key="code_versionamento_nao")
            with col3:
                st.session_state.form_data['code_versionamento_obs'] = st.text_input(
                    _("Observações"),
                    key="obs_versionamento",
                    label_visibility="collapsed"
                )
            st.session_state.form_data['code_versionamento'] = "Sim" if sim else "Não" if nao else None

            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button(_("Anterior")):
                    st.session_state.page = 3
            with col2:
                if st.form_submit_button(_("Próximo"), type="primary"):
                    st.session_state.page = 5

    def _render_extra_validations(self):
        st.header(_("Validações Extras"))
        with st.form("validacoes_adicionais"):
            st.write(_("Acessibilidade foi considerada (uso de leitores de tela, contraste adequado, navegação por teclado)?"))
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                sim = st.checkbox(_("Sim"), key="extra_acessibilidade_sim")
            with col2:
                nao = st.checkbox(_("Não"), key="extra_acessibilidade_nao")
            with col3:
                st.session_state.form_data['extra_acessibilidade_obs'] = st.text_input(
                    _("Observações"),
                    key="obs_acessibilidade",
                    label_visibility="collapsed"
                )
            st.session_state.form_data['extra_acessibilidade'] = "Sim" if sim else "Não" if nao else None
            st.markdown("---")

            st.write(_("Performance da interface e tempo de carregamento estão aceitáveis?"))
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                sim = st.checkbox(_("Sim"), key="extra_performance_sim")
            with col2:
                nao = st.checkbox(_("Não"), key="extra_performance_nao")
            with col3:
                st.session_state.form_data['extra_performance_obs'] = st.text_input(
                    _("Observações"),
                    key="obs_performance",
                    label_visibility="collapsed"
                )
            st.session_state.form_data['extra_performance'] = "Sim" if sim else "Não" if nao else None
            st.markdown("---")

            st.write(_("Não foram identificados bugs visuais ou funcionais críticos?"))
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                sim = st.checkbox(_("Sim"), key="extra_bugs_sim")
            with col2:
                nao = st.checkbox(_("Não"), key="extra_bugs_nao")
            with col3:
                st.session_state.form_data['extra_bugs_obs'] = st.text_input(
                    _("Observações"),
                    key="obs_bugs",
                    label_visibility="collapsed"
                )
            st.session_state.form_data['extra_bugs'] = "Sim" if sim else "Não" if nao else None

            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button(_("Anterior")):
                    st.session_state.page = 4
            with col2:
                if st.form_submit_button(_("Próximo"), type="primary"):
                    st.session_state.page = 6

    def _render_feedback(self):
        st.header(_("Feedback"))
        with st.form("feedback"):
            st.subheader(_("Pontos Positivos"))
            st.session_state.form_data['feedback_pontos_positivos'] = st.text_area(
                _("Pontos Positivos"),
                placeholder=_("Liste os pontos positivos identificados"),
                label_visibility="collapsed"
            )

            st.subheader(_("Pontos de Melhoria"))
            st.session_state.form_data['feedback_pontos_melhoria'] = st.text_area(
                _("Pontos de Melhoria"),
                placeholder=_("Liste os pontos que precisam ser melhorados"),
                label_visibility="collapsed"
            )

            st.subheader(_("Aprovação Final"))
            col1, col2 = st.columns(2)
            with col1:
                aprovado = st.checkbox(_("Aprovado"), key="feedback_aprovado")
            with col2:
                reprovado = st.checkbox(_("Reprovado - Necessita Ajustes"), key="feedback_reprovado")
            
            if aprovado and reprovado:
                st.error(_("Por favor, selecione apenas uma opção de aprovação"))
            st.session_state.form_data['feedback_aprovacao'] = "Aprovado" if aprovado else "Reprovado - Necessita Ajustes" if reprovado else None

            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button(_("Anterior")):
                    st.session_state.page = 5
            with col2:
                if st.form_submit_button(_("Próximo"), type="primary"):
                    if st.session_state.form_data.get('feedback_aprovacao') is not None:
                        st.session_state.page = 7
                    else:
                        st.error(_("Por favor, selecione a aprovação final!"))

    def _render_success(self):
        st.header(_("Avaliação Concluída"))
        st.write(_("Agradecemos por completar a avaliação!"))
        st.write(_("Seu feedback é muito importante para nós."))

        self.generate_report()

        with st.form("success_form"):
            if st.form_submit_button(_("Gerar novo relatório")):
                st.session_state.form_data = {}
                st.session_state.form_data = {}
                st.session_state.page = 1

    def generate_report(self):
        pdf_generator = PDFGenerator(st.session_state.form_data)
        
        pdf_bytes = pdf_generator.generate_pdf()

        task_id = st.session_state.form_data.get('id_tarefa', '').strip()
        if not task_id:
            task_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            
        filename = f"qa-test-report-{task_id}.pdf"
        
        st.download_button(
            label=_("Baixar Relatório"),
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
            type="primary"
        ) 