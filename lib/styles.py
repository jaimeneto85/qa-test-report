def get_css():
    return """
        <style>
            /* Botões de navegação */
            div[data-testid="column"] div[data-testid="stForm"] {
                max-width: 230px !important;
            }
            
            /* Container de sucesso */
            .success-container {
                padding: 20px;
                background-color: #f0f8f0;
                border-radius: 10px;
                text-align: center;
            }
            
            /* Linha divisória entre itens do formulário */
            .form-divider {
                border-bottom: 1px solid #e6e6e6;
                margin-top: 5px;
                margin-bottom: 15px;
            }
            .stHorizontalBlock{
                margin-top: 2em;
            }

            .stHorizontalBlock:last-child .stColumn{
                flex: 1;
                justify-content: space-between;
                max-width: 230px !important;
            }

            .stColumn button {
                flex:1;
            }

            button[kind="primaryFormSubmit"] {
                background: #0d6efd;
                border: none;
            }
            button[kind="primaryFormSubmit"]:hover {
                background: #0d6ecd;
                border: none;
            }
            button[kind="primaryFormSubmit"]:active {
                background: #0d6ecd;
                border: none;
                color: white;
            }
            .stHorizontalBlock{
                display:flex;
                justify-content: space-between;
            }
        </style>
    """ 