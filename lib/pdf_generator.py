from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .form_data import QAFormData

class PDFGenerator:
    def __init__(self, data: QAFormData):
        self.data = data
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=30
        )

    def generate_pdf(self, filename: str):
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        
        elements.append(Paragraph('Formulário de Validação da Entrega – QA/Engenharia de Testes', self.title_style))
        elements.extend(self._add_basic_info())
        elements.extend(self._add_sections())
        elements.extend(self._add_feedback())
        
        doc.build(elements)
        return filename

    def _add_basic_info(self):
        elements = []
        data_dict = self.data.to_dict()
        for key, value in {
            'Data da Avaliação': data_dict["data_avaliacao"],
            'Nome do Avaliador': data_dict["nome_avaliador"],
            'Nome do Engenheiro': data_dict["nome_engenheiro"],
            'Funcionalidade/Entrega': data_dict["funcionalidade"],
            'Versão do Produto': data_dict["versao"],
            'Identificação da Tarefa': data_dict["id_tarefa"]
        }.items():
            elements.append(Paragraph(f"{key}: {value}", self.styles['Normal']))
            elements.append(Spacer(1, 12))
        return elements

    def _add_sections(self):
        elements = []
        sections = {
            'Conformidade com o Design UX/UI': self.data.ux_ui,
            'Funcionalidade e Comportamento': self.data.codigo,
            'Qualidade do Código e Testabilidade': self.data.funcionalidade_respostas,
            'Validações Extras': self.data.validacoes
        }
        
        for title, section_data in sections.items():
            elements.extend(self._create_section(title, section_data))
        return elements

    def _create_section(self, title, section_data):
        elements = []
        elements.append(Paragraph(title, self.styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        table_data = [['Critério', 'Sim', 'Não', 'Observações']]
        for item in section_data:
            table_data.append([
                item['criterio'],
                '☑' if item['valor'] else '',
                '☑' if not item['valor'] else '',
                item['observacao']
            ])
        
        t = Table(table_data, colWidths=[250, 50, 50, 150])
        t.setStyle(self._get_table_style())
        elements.append(t)
        elements.append(Spacer(1, 20))
        return elements

    def _get_table_style(self):
        return TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

    def _add_feedback(self):
        elements = []
        elements.append(Paragraph('Feedback Geral', self.styles['Heading2']))
        elements.append(Paragraph(f"Pontos Positivos: {self.data.pontos_positivos}", self.styles['Normal']))
        elements.append(Paragraph(f"Pontos de Melhoria: {self.data.pontos_melhoria}", self.styles['Normal']))
        
        aprovacao = 'Aprovado' if self.data.aprovacao else 'Reprovado – Necessita Ajustes'
        elements.append(Paragraph(f"Aprovação Final: ☑ {aprovacao}", self.styles['Normal']))
        elements.append(Paragraph(f"Assinatura do QA/Engenheiro de Testes: {self.data.nome_avaliador}", self.styles['Normal']))
        return elements 