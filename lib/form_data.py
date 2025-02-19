from datetime import datetime

class QAFormData:
    def __init__(self):
        self.data_avaliacao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.nome_avaliador = ""
        self.nome_engenheiro = ""
        self.funcionalidade = ""
        self.versao = ""
        self.id_tarefa = ""
        self.ux_ui = []
        self.funcionalidade_respostas = []
        self.codigo = []
        self.validacoes = []
        self.pontos_positivos = ""
        self.pontos_melhoria = ""
        self.aprovacao = False

    def to_dict(self):
        return {
            "data_avaliacao": self.data_avaliacao,
            "nome_avaliador": self.nome_avaliador,
            "nome_engenheiro": self.nome_engenheiro,
            "funcionalidade": self.funcionalidade,
            "versao": self.versao,
            "id_tarefa": self.id_tarefa,
            "ux_ui": self.ux_ui,
            "funcionalidade": self.funcionalidade_respostas,
            "codigo": self.codigo,
            "validacoes": self.validacoes,
            "pontos_positivos": self.pontos_positivos,
            "pontos_melhoria": self.pontos_melhoria,
            "aprovacao": self.aprovacao
        } 