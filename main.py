import customtkinter as ctk
import mysql.connector
import pandas as pd
import os
import threading
import requests



def processar_consulta():
    inicio = entrada_inicio.get()
    fim = entrada_fim.get()
    tipo_consulta = opcao_tipo.get()

    try:
        ids =  entrada_ids.get().split(',')
    except ValueError:
        resultado_label.configure(text="IDs inválidos. Certifique-se de separar por vírgulas.", text_color="red")
        return
    
    params = {
        'inicio': inicio,
        'fim': fim,
        'ids': ','.join(ids), 
        'tipo_consulta': tipo_consulta
    }
    
    url = 'https://n8n.zapisp.com.br/webhook-test/338bf7f8-75f1-48da-915c-39c21ddb1d9b'
    
    response = requests.get(url, params=params)
    
    if isinstance(dados, list) and all(isinstance(item, dict) for item in dados):
        dados = response.json()
        df = pd.DataFrame(dados)
        df.to_csv("dados_consulta.csv", index=False)
        print("Dados salvos com sucesso no arquivo 'dados_consulta.csv'")
    else:
        print(f"Erro ao fazer o request: {response.status_code} - {response.text}")

# Configuração do banco de dados
db_username = 'suporte'
db_password = 'LewSG907$yX5'
db_host = 'mysql-zapisp-prod.cayxp5jpjfif.us-east-1.rds.amazonaws.com'
db_database = 'zapisp'

# Configurações da janela principal
ctk.set_appearance_mode("dark")  # Modos: "dark" ou "light"
ctk.set_default_color_theme("blue")  # Tema: "blue", "green", "dark-blue"

janela = ctk.CTk()
janela.title("Consulta de Dados")
janela.geometry("400x350")

# Componentes da interface
titulo_label = ctk.CTkLabel(janela, text="Consulta de Dados", font=("Arial", 18))
titulo_label.pack(pady=10)

inicio_label = ctk.CTkLabel(janela, text="Data de Início:")
inicio_label.pack()
entrada_inicio = ctk.CTkEntry(janela, placeholder_text = "AAAA-MM-DD")
entrada_inicio.pack()

fim_label = ctk.CTkLabel(janela, text="Data de Fim:")
fim_label.pack()
entrada_fim = ctk.CTkEntry(janela, placeholder_text = "AAAA-MM-DD")
entrada_fim.pack()

ids_label = ctk.CTkLabel(janela, text="IDs das Empresas (separados por vírgula):")
ids_label.pack()
entrada_ids = ctk.CTkEntry(janela)
entrada_ids.pack()

tipo_label = ctk.CTkLabel(janela, text="Tipo de Consulta:")
tipo_label.pack()
opcao_tipo = ctk.CTkComboBox(janela, values=["Campanha", "Gateway", "Healthscore"])
opcao_tipo.pack()

consultar_botao = ctk.CTkButton(janela, text="Consultar", command=processar_consulta)
consultar_botao.pack(pady=10)

resultado_label = ctk.CTkLabel(janela, text="")
resultado_label.pack()

# Executa a janela
janela.mainloop()
