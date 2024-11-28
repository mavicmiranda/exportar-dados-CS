import requests
import pandas as pd
from tkinter.filedialog import asksaveasfilename
import customtkinter as ctk


def processar_consulta():
    inicio = entrada_inicio.get()
    fim = entrada_fim.get()
    tipo_consulta = opcao_tipo.get()
    
    url_health = 'https://queue-ms-3000.zapisp.com.br/health'
    
    try:
        response_health = requests.get(url_health, headers={'accept': 'application/json'})
        if response_health.status_code == 200:
            print("Permissão concedida, prosseguindo com a segunda requisição.")
        else:
            print(f"Permissão negada. Código de status: {response_health.status_code}")
            resultado_label.configure(text="Permissão de acesso negada", text_color="red")
            return
    except requests.RequestException as e:
        print(f"Erro ao verificar permissão: {e}")
        return

    try:
        ids = entrada_ids.get().split(',')
    except ValueError:
        resultado_label.configure(text="IDs inválidos. Certifique-se de separar por vírgulas.", text_color="red")
        return

    params = {
        'inicio': inicio,
        'fim': fim,
        'ids': ','.join(ids),
        'tipo_consulta': tipo_consulta
    }

    url = 'https://n8n.zapisp.com.br/webhook/338bf7f8-75f1-48da-915c-39c21ddb1d9b'

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao fazer a requisição: {e}")
        resultado_label.configure(text="Erro ao fazer a requisição.", text_color="red")
        return

    try:
        dados = response.json()
    except ValueError:
        print(f"Erro ao decodificar JSON: {response.text}")
        resultado_label.configure(text="Erro ao processar a resposta do servidor.", text_color="red")
        return

    if isinstance(dados, dict):  
        dados = [dados]
    elif not isinstance(dados, list):
        print(f"Resposta inválida: {dados}")
        resultado_label.configure(text="Dados retornados inválidos.", text_color="red")
        return

    if all(isinstance(item, dict) for item in dados):
        try:
            # Abrir a janela para salvar o arquivo
            arquivo = asksaveasfilename(
                defaultextension=".csv",  # Extensão padrão
                filetypes=[("CSV files", "*.csv")],  # Tipos de arquivos permitidos
                initialfile="dados_consulta.csv",  # Nome padrão
                title="Salvar arquivo como"  # Título da janela
            )
            # Verificar se o usuário selecionou um arquivo
            if arquivo:
                df = pd.DataFrame(dados)
                df.to_csv(arquivo, index=False)
                print(f"Dados salvos com sucesso no arquivo '{arquivo}'")
                resultado_label.configure(text="Dados salvos com sucesso no CSV!", text_color="green")
            else:
                print("Ação cancelada pelo usuário.")
                resultado_label.configure(text="Ação cancelada.", text_color="orange")
        except Exception as e:
            print(f"Erro ao salvar os dados no CSV: {e}")
            resultado_label.configure(text="Erro ao salvar os dados no CSV.", text_color="red")
    else:
        print(f"Erro ao processar os dados.")
        resultado_label.configure(text="Erro ao processar os dados.", text_color="red")


# Configurações da janela principal
ctk.set_appearance_mode("dark")  # Modos: "dark" ou "light"
ctk.set_default_color_theme("blue")  # Tema: "blue", "green", "dark-blue"

janela = ctk.CTk()
janela.title("Exportar Dados")
janela.geometry("400x350")

# Componentes da interface
titulo_label = ctk.CTkLabel(janela, text="Exportar Dados", font=("Arial", 18))
titulo_label.pack(pady=10)

inicio_label = ctk.CTkLabel(janela, text="Data de Início:")
inicio_label.pack()
entrada_inicio = ctk.CTkEntry(janela, placeholder_text="AAAA-MM-DD")
entrada_inicio.pack()

fim_label = ctk.CTkLabel(janela, text="Data de Fim:")
fim_label.pack()
entrada_fim = ctk.CTkEntry(janela, placeholder_text="AAAA-MM-DD")
entrada_fim.pack()

ids_label = ctk.CTkLabel(janela, text="IDs das Empresas (separados por vírgula):")
ids_label.pack()
entrada_ids = ctk.CTkEntry(janela)
entrada_ids.pack()

tipo_label = ctk.CTkLabel(janela, text="Tipo de Consulta:")
tipo_label.pack()
opcao_tipo = ctk.CTkComboBox(janela, values=["Campanha", "Gateway", "Healthscore"])
opcao_tipo.pack()

consultar_botao = ctk.CTkButton(janela, text="Exportar", command=processar_consulta)
consultar_botao.pack(pady=10)

resultado_label = ctk.CTkLabel(janela, text="")
resultado_label.pack()

# Executa a janela
janela.mainloop()
