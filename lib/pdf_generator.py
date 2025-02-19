from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
from datetime import datetime
from .translations import _, set_language

class PDFGenerator:
    def __init__(self, form_data):
        self.form_data = form_data
        self.buffer = BytesIO()
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=TA_CENTER
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=20
        )
        self.normal_style = self.styles['Normal']
        
    def generate_pdf(self):
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        story.append(Paragraph(_("Formulário de Validação da Entrega – QA/Engenharia de Testes"), self.title_style))
        story.append(Spacer(1, 20))
        
        story.extend(self._create_basic_info())
        story.append(Spacer(1, 20))
        
        story.extend(self._create_ux_ui_section())
        story.append(Spacer(1, 20))
        
        story.extend(self._create_functionality_section())
        story.append(Spacer(1, 20))
        
        story.extend(self._create_code_quality_section())
        story.append(Spacer(1, 20))
        
        story.extend(self._create_extra_validations_section())
        story.append(Spacer(1, 20))
        
        story.extend(self._create_feedback_section())
        
        doc.build(story)
        
        pdf = self.buffer.getvalue()
        self.buffer.close()
        
        return pdf
        
    def _create_basic_info(self):
        elements = []
        data = [
            [_("Data da Avaliação"), self.form_data.get('data_avaliacao', '')],
            [_("Nome do Avaliador"), self.form_data.get('nome_avaliador', '')],
            [_("Nome do Engenheiro"), self.form_data.get('nome_engenheiro', '')],
            [_("Funcionalidade/Entrega"), self.form_data.get('funcionalidade', '')],
            [_("Versão do Produto"), self.form_data.get('versao', '')],
            [_("ID da Tarefa"), self.form_data.get('id_tarefa', '')]
        ]
        
        table = Table(data, colWidths=[200, 300])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(table)
        return elements
        
    def _create_section_table(self, title, criteria_data):
        elements = []
        elements.append(Paragraph(title, self.heading_style))
        
        data = [[_("Critério"), _("Sim"), _("Não"), _("Observações")]]
        
        for criterion in criteria_data:
            data.append([
                criterion['text'],
                '☑' if criterion['response'] == 'Sim' else '☐',
                '☑' if criterion['response'] == 'Não' else '☐',
                criterion['obs']
            ])
            
        table = Table(data, colWidths=[250, 50, 50, 150])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(table)
        return elements
        
    def _create_ux_ui_section(self):
        criteria = [
            {
                'text': _("A entrega está 100% alinhada ao protótipo/UI design (Figma, Zeplin, etc)?"),
                'response': self.form_data.get('ux_ui_alinhamento', ''),
                'obs': self.form_data.get('ux_ui_alinhamento_obs', '')
            },
            {
                'text': _("As cores, fontes, ícones e espaçamentos seguem o guia de estilo da empresa?"),
                'response': self.form_data.get('ux_ui_guia_estilo', ''),
                'obs': self.form_data.get('ux_ui_guia_estilo_obs', '')
            },
            {
                'text': _("Componentes reutilizáveis e padrões de design foram respeitados?"),
                'response': self.form_data.get('ux_ui_componentes', ''),
                'obs': self.form_data.get('ux_ui_componentes_obs', '')
            },
            {
                'text': _("Experiência do usuário (UX) é fluida e sem pontos de atrito?"),
                'response': self.form_data.get('ux_ui_experiencia', ''),
                'obs': self.form_data.get('ux_ui_experiencia_obs', '')
            },
            {
                'text': _("Transições, animações e interações estão implementadas conforme especificado?"),
                'response': self.form_data.get('ux_ui_transicoes', ''),
                'obs': self.form_data.get('ux_ui_transicoes_obs', '')
            }
        ]
        return self._create_section_table(_("Conformidade com o Design UX/UI"), criteria)
        
    def _create_functionality_section(self):
        criteria = [
            {
                'text': _("Todos os fluxos funcionam conforme esperado e especificado no UX?"),
                'response': self.form_data.get('func_fluxos', ''),
                'obs': self.form_data.get('func_fluxos_obs', '')
            },
            {
                'text': _("Campos de formulário, botões e interações respondem corretamente?"),
                'response': self.form_data.get('func_campos', ''),
                'obs': self.form_data.get('func_campos_obs', '')
            },
            {
                'text': _("Tratamento de erros e mensagens de validação estão implementados e alinhados ao design?"),
                'response': self.form_data.get('func_erros', ''),
                'obs': self.form_data.get('func_erros_obs', '')
            },
            {
                'text': _("Comportamento responsivo (mobile, tablet, desktop) foi validado?"),
                'response': self.form_data.get('func_responsivo', ''),
                'obs': self.form_data.get('func_responsivo_obs', '')
            },
            {
                'text': _("Funcionalidade foi testada em diferentes navegadores e sistemas operacionais?"),
                'response': self.form_data.get('func_navegadores', ''),
                'obs': self.form_data.get('func_navegadores_obs', '')
            }
        ]
        return self._create_section_table(_("Funcionalidade e Comportamento"), criteria)
        
    def _create_code_quality_section(self):
        criteria = [
            {
                'text': _("Código segue os padrões internos e boas práticas de desenvolvimento?"),
                'response': self.form_data.get('code_padroes', ''),
                'obs': self.form_data.get('code_padroes_obs', '')
            },
            {
                'text': _("Há cobertura de testes unitários e de integração para as principais partes da funcionalidade?"),
                'response': self.form_data.get('code_testes', ''),
                'obs': self.form_data.get('code_testes_obs', '')
            },
            {
                'text': _("Casos de teste automatizados foram implementados ou documentados?"),
                'response': self.form_data.get('code_automatizados', ''),
                'obs': self.form_data.get('code_automatizados_obs', '')
            },
            {
                'text': _("A entrega está devidamente versionada e integrada com o repositório?"),
                'response': self.form_data.get('code_versionamento', ''),
                'obs': self.form_data.get('code_versionamento_obs', '')
            }
        ]
        return self._create_section_table(_("Qualidade do Código e Testabilidade"), criteria)
        
    def _create_extra_validations_section(self):
        criteria = [
            {
                'text': _("Acessibilidade foi considerada (uso de leitores de tela, contraste adequado, navegação por teclado)?"),
                'response': self.form_data.get('extra_acessibilidade', ''),
                'obs': self.form_data.get('extra_acessibilidade_obs', '')
            },
            {
                'text': _("Performance da interface e tempo de carregamento estão aceitáveis?"),
                'response': self.form_data.get('extra_performance', ''),
                'obs': self.form_data.get('extra_performance_obs', '')
            },
            {
                'text': _("Não foram identificados bugs visuais ou funcionais críticos?"),
                'response': self.form_data.get('extra_bugs', ''),
                'obs': self.form_data.get('extra_bugs_obs', '')
            }
        ]
        return self._create_section_table(_("Validações Extras"), criteria)
        
    def _create_feedback_section(self):
        elements = []
        elements.append(Paragraph(_("Feedback Geral"), self.heading_style))
        
        elements.append(Paragraph(_("Pontos Positivos:"), self.normal_style))
        elements.append(Paragraph(self.form_data.get('feedback_pontos_positivos', ''), self.normal_style))
        elements.append(Spacer(1, 10))
        
        elements.append(Paragraph(_("Pontos de Melhoria:"), self.normal_style))
        elements.append(Paragraph(self.form_data.get('feedback_pontos_melhoria', ''), self.normal_style))
        elements.append(Spacer(1, 20))
        
        approval = self.form_data.get('feedback_aprovacao', '')
        elements.append(Paragraph(_("Aprovação Final: {}").format(approval), self.normal_style))
        elements.append(Spacer(1, 20))
        
        elements.append(Paragraph("_" * 50, self.normal_style))
        elements.append(Paragraph(self.form_data.get('nome_avaliador', ''), self.normal_style))
        elements.append(Paragraph(_("QA/Engenheiro de Testes"), self.normal_style))
            
        return elements