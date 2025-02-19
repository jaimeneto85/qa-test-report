import streamlit as st
from lib import QAFormData, PDFGenerator
from datetime import datetime
from lib.styles import get_css
import os

class QAFormUI:
    def __init__(self):
        self.form_data = QAFormData()
        if 'page' not in st.session_state:
            st.session_state.page = 1
            st.session_state.form_data = {}
        # Inject CSS once at startup
        st.markdown(get_css(), unsafe_allow_html=True)
        # Ensure reports directory exists
        self.reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)

    def render(self):
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

    def _render_header(self):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.title("Formulário de Validação QA")
        with col2:
            st.progress(st.session_state.page/7, f"Etapa {st.session_state.page}/7")

    def _collect_basic_info(self):
        st.session_state.form_data['data_avaliacao'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        st.session_state.form_data['nome_avaliador'] = st.text_input("Nome do Avaliador", placeholder="Nome do avaliador")
        st.session_state.form_data['nome_engenheiro'] = st.text_input("Nome do Engenheiro", placeholder="Nome do engenheiro responsável pela entrega")
        st.session_state.form_data['funcionalidade'] = st.text_input("Funcionalidade/Entrega", placeholder="Qual funcionalidade ou entrega foi validada?")
        st.session_state.form_data['versao'] = st.text_input("Versão do Produto", placeholder="Versão do produto no pacote ou do release a ser lançado")
        st.session_state.form_data['id_tarefa'] = st.text_input("Identificação da Tarefa", placeholder="ID da Tarefa")

    def _validate_basic_info(self):
        return all([
            st.session_state.form_data.get('nome_avaliador'),
            st.session_state.form_data.get('nome_engenheiro'),
            st.session_state.form_data.get('funcionalidade'),
            st.session_state.form_data.get('versao'),
            st.session_state.form_data.get('id_tarefa')
        ])

    def _render_basic_info(self):
        st.header("Informações Básicas")
        with st.form("info_basica"):
            self._collect_basic_info()
            if st.form_submit_button("Próximo"):
                if self._validate_basic_info():
                    st.session_state.page = 2
                else:
                    st.error("Por favor, preencha todos os campos!")

    def _render_form_item(self, criterio, valor_key, observacao_key, is_last=False):
        col1, col2 = st.columns([3, 1])
        with col1:
            valor = st.checkbox(criterio, key=valor_key)
        with col2:
            observacao = st.text_input("Observação", key=observacao_key)
            
        if not is_last:
            st.markdown("""
                <div class="form-divider"></div>
            """, unsafe_allow_html=True)
        
        return valor, observacao

    def _render_form_section(self, title, form_id, criterios, state_key, next_page, prev_page):
        st.header(title)
        
        with st.form(form_id, clear_on_submit=True):
            responses = []
            for i, criterio in enumerate(criterios):
                valor, observacao = self._render_form_item(
                    criterio,
                    f"valor_{form_id}_{i}",
                    f"obs_{form_id}_{i}",
                    is_last=(i == len(criterios) - 1)
                )
                responses.append({
                    "criterio": criterio,
                    "valor": valor,
                    "observacao": observacao
                })
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.form_submit_button("Voltar", use_container_width=True):
                    st.session_state.page = prev_page
                    st.rerun()
            with col2:
                if st.form_submit_button("Próximo", type="primary", use_container_width=True, ):
                    st.session_state.form_data[state_key] = responses
                    st.session_state.page = next_page
                    st.rerun()

    def _render_ux_ui(self):
        self._render_form_section(
            "Conformidade com Design UX/UI",
            "ux_ui",
            [
                'A entrega está 100% alinhada ao protótipo/UI design (Figma, Zeplin, etc)?',
                'As cores, fontes, ícones e espaçamentos seguem o guia de estilo da empresa?',
                'Componentes reutilizáveis e padrões de design foram respeitados?',
                'Experiência do usuário (UX) é fluida e sem pontos de atrito?',
                'Transições, animações e interações estão implementadas conforme especificado?'
            ],
            'ux_ui',
            3,
            1
        )

    def _render_functionality(self):
        self._render_form_section(
            "Funcionalidade e Comportamento",
            "func",
            [
                'Todos os fluxos funcionam conforme esperado e especificado no UX?',
                'Campos de formulário, botões e interações respondem corretamente?',
                'Tratamento de erros e mensagens de validação estão implementados e alinhados ao design?',
                'Comportamento responsivo (mobile, tablet, desktop) foi validado?',
                'Funcionalidade foi testada em diferentes navegadores e sistemas operacionais?'
            ],
            'funcionalidade',
            4,
            2
        )

    def _render_code_quality(self):
        self._render_form_section(
            "Qualidade do Código e Testabilidade",
            "code",
            [
                'Código segue os padrões internos e boas práticas de desenvolvimento?',
                'Há cobertura de testes unitários e de integração para as principais partes da funcionalidade?',
                'Casos de teste automatizados foram implementados ou documentados?',
                'A entrega está devidamente versionada e integrada com o repositório?'
            ],
            'codigo',
            5,
            3
        )

    def _render_extra_validations(self):
        self._render_form_section(
            "Validações Extras",
            "extra",
            [
                'Acessibilidade foi considerada (uso de leitores de tela, contraste adequado, navegação por teclado)?',
                'Performance da interface e tempo de carregamento estão aceitáveis?',
                'Não foram identificados bugs visuais ou funcionais críticos?'
            ],
            'validacoes',
            6,
            4
        )

    def _render_feedback(self):
        st.header("Feedback Final")
        
        with st.form("feedback_form"):
            st.session_state.form_data['pontos_positivos'] = st.text_area("Pontos Positivos")
            st.session_state.form_data['pontos_melhoria'] = st.text_area("Pontos de Melhoria")
            
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.form_data['aprovacao'] = st.checkbox("Aprovado")
            with col2:
                if not st.session_state.form_data.get('aprovacao'):
                    st.write(" ")
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.form_submit_button("Voltar", use_container_width=True):
                    st.session_state.page = 5
                    st.rerun()
            with col2:
                if st.form_submit_button("Finalizar", type="primary", use_container_width=True):
                    st.session_state.page = 7
                    st.rerun()

    def _render_success(self):
        st.balloons()
        
        success_container = st.container()
        with success_container:
            st.markdown("""
            <div class="success-container">
                <h2>🎉 Parabéns!</h2>
                <p style='font-size: 18px;'>Você completou o formulário de validação com sucesso!</p>
            </div>
            """, unsafe_allow_html=True)
            
            pdf_path = self._generate_pdf()
            
            col1, col2 = st.columns(2)
            with col1:
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="📥 Baixar Relatório PDF",
                        data=pdf_file,
                        file_name=pdf_path,
                        mime="application/pdf",
                        type="primary"
                    )
            with col2:
                if st.button("✨ Novo Relatório", type="secondary"):
                    st.session_state.page = 1
                    st.session_state.form_data = {}
                    st.rerun()

    def _generate_pdf(self):
        pdf_generator = PDFGenerator(self.form_data)
        filename = f"formulario_validacao_qa_{self.form_data.id_tarefa}.pdf"
        pdf_path = os.path.join(self.reports_dir, filename)
        return pdf_generator.generate_pdf(pdf_path)

def main():
    st.set_page_config(page_title="Formulário de Validação QA", layout="wide")
    app = QAFormUI()
    app.render()

if __name__ == "__main__":
    main() 