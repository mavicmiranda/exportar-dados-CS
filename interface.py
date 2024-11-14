import customtkinter as ctk
import mysql.connector
import pandas as pd
import os
import threading



def carregar_query(arquivo_sql, inicio, fim, lote_ids):
    with open(arquivo_sql, 'r') as file:
        query = file.read()
    query = query.format(inicio=inicio, fim=fim, ids=', '.join(map(str, lote_ids)))
    return query

def consultar_dados():
    # Exibe a mensagem de "loading" para o usuário
    resultado_label.configure(text="Carregando, por favor aguarde...", text_color="blue")
    resultado_label.update_idletasks()  # Atualiza a interface imediatamente para exibir a mensagem
    
    # Executa a consulta em uma nova thread para não bloquear a interface
    thread = threading.Thread(target=processar_consulta)
    thread.start()

def processar_consulta():
    inicio = entrada_inicio.get()
    fim = entrada_fim.get()
    tipo_consulta = opcao_tipo.get()
    arquivo_sql = consulta_map.get(tipo_consulta)

    if not arquivo_sql:
        resultado_label.configure(text="Selecione um tipo de consulta válido.", text_color="red")
        return

    try:
        ids = list(map(int, entrada_ids.get().split(',')))
    except ValueError:
        resultado_label.configure(text="IDs inválidos. Certifique-se de separar por vírgulas.", text_color="red")
        return

    lote_tamanho = 10
    try:
        connection = mysql.connector.connect(
            host=db_host,
            database=db_database,
            user=db_username,
            password=db_password
        )
        cursor = connection.cursor(dictionary=True)

        df_resultado = pd.DataFrame()
        
        for i in range(0, len(ids), lote_tamanho):
            lote_ids = ids[i:i + lote_tamanho]
            query = carregar_query(arquivo_sql, inicio, fim, lote_ids)
            cursor.execute(query)
            resultados = cursor.fetchall()
            df_resultado = pd.concat([df_resultado, pd.DataFrame(resultados)], ignore_index=True)

        # Salva o DataFrame no arquivo CSV
        df_resultado.to_csv(f'dados_{tipo_consulta}_{inicio}_{fim}.csv', index=False)
        
        # Atualiza o rótulo para indicar sucesso
        resultado_label.configure(text="Dados exportados com sucesso!", text_color="green")

    except mysql.connector.Error as error:
        resultado_label.configure(text=f"Erro ao conectar ao banco de dados: {error}", text_color="red")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            
    # Obtendo os parâmetros de entrada
    inicio = entrada_inicio.get()
    fim = entrada_fim.get()
    tipo_consulta = opcao_tipo.get()
    arquivo_sql = consulta_map.get(tipo_consulta)

    if not arquivo_sql:
        resultado_label.configure(text="Selecione um tipo de consulta válido.", text_color="red")
        return

    # Obtendo os IDs a partir do campo de entrada e convertendo em lista de inteiros
    try:
        ids = list(map(int, entrada_ids.get().split(',')))
    except ValueError:
        resultado_label.configure(text="IDs inválidos. Certifique-se de separar por vírgulas.", text_color="red")
        return

    lote_tamanho = 10

    try:
        # Conectando ao banco de dados
        connection = mysql.connector.connect(
            host=db_host,
            database=db_database,
            user=db_username,
            password=db_password
        )
        cursor = connection.cursor(dictionary=True)

        # DataFrame para armazenar os resultados
        df_resultado = pd.DataFrame()
        
        # Processando os IDs em lotes
        for i in range(0, len(ids), lote_tamanho):
            lote_ids = ids[i:i + lote_tamanho]
            # Chamando a função carregar_query para obter a query formatada
            query = carregar_query(arquivo_sql, inicio, fim, lote_ids)
            
            # Executando a consulta no banco de dados
            cursor.execute(query)
            resultados = cursor.fetchall()

            # Convertendo os resultados para DataFrame e concatenando
            df_resultado = pd.concat([df_resultado, pd.DataFrame(resultados)], ignore_index=True)

        # Salvando os resultados em um arquivo CSV
        df_resultado.to_csv(f'dados_{tipo_consulta}_{inicio}_{fim}.csv', index=False)

        # Atualizando o rótulo de sucesso
        resultado_label.configure(text="Dados exportados com sucesso!", text_color="green")

    except mysql.connector.Error as error:
        # Caso ocorra um erro na conexão
        resultado_label.configure(text=f"Erro ao conectar ao banco de dados: {error}", text_color="red")

    finally:
        # Fechando a conexão com o banco de dados
        if connection.is_connected():
            cursor.close()
            connection.close()

# Configuração do banco de dados
db_username = 'suporte'
db_password = 'LewSG907$yX5'
db_host = 'mysql-zapisp-prod.cayxp5jpjfif.us-east-1.rds.amazonaws.com'
db_database = 'zapisp'

# Caminho para arquivos SQL
current_dir = os.path.dirname(os.path.abspath(__file__))
consulta_map = {
    "Campanha": os.path.join(current_dir, "campanha.sql"),
    "Gateway": os.path.join(current_dir, "gateway.sql"),
    "Healthscore": os.path.join(current_dir, "healthscore.sql")
}

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

consultar_botao = ctk.CTkButton(janela, text="Consultar", command=consultar_dados)
consultar_botao.pack(pady=10)

resultado_label = ctk.CTkLabel(janela, text="")
resultado_label.pack()

# Executa a janela
janela.mainloop()
