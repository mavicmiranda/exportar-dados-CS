import os
import requests
from dotenv import load_dotenv
import pandas as pd
from tkinter.filedialog import asksaveasfilename
import customtkinter as ctk
from PIL import Image
import os
from dotenv import load_dotenv

url_health = os.getenv("URL_HEALTH")
url = os.getenv("WEBHOOK_URL")
load_dotenv()


def processar_consulta():
    inicio = entrada_inicio.get()
    fim = entrada_fim.get()
    tipo_consulta = opcao_tipo.get()

    url_health = os.getenv("URL_HEALTH")
    url = os.getenv("WEBHOOK_URL")
    
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

    url = os.getenv("WEBHOOK_URL")

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
            arquivo = asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                initialfile="dados_consulta.csv",
                title="Salvar arquivo como"
            )
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

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("Exportar Dados")
janela.geometry("400x600")

janela.iconbitmap("icon.ico")

imagem = ctk.CTkImage(light_image=Image.open("logo.png"), size=(200, 100))
imagem_label = ctk.CTkLabel(janela, image=imagem, text="")
imagem_label.pack(pady=10, fill="x")

frame_inputs = ctk.CTkFrame(janela)
frame_inputs.pack(fill="both", expand=True, padx=20, pady=10)

inicio_label = ctk.CTkLabel(frame_inputs, text="Data de Início:", anchor="w")
inicio_label.pack(fill="x", anchor="w", pady=5, padx=20)
entrada_inicio = ctk.CTkEntry(frame_inputs, placeholder_text="AAAA-MM-DD")
entrada_inicio.pack(fill="x", pady=5, padx=20)

fim_label = ctk.CTkLabel(frame_inputs, text="Data de Fim:", anchor="w")
fim_label.pack(fill="x", anchor="w", padx=20)
entrada_fim = ctk.CTkEntry(frame_inputs, placeholder_text="AAAA-MM-DD")
entrada_fim.pack(fill="x", pady=5, padx=20)

ids_label = ctk.CTkLabel(frame_inputs, text="IDs das Empresas:", anchor="w")
ids_label.pack(fill="x", anchor="w", padx=20)
entrada_ids = ctk.CTkEntry(frame_inputs, placeholder_text="separados por vírgula ex.: 48, 49, 50...")
entrada_ids.pack(fill="x", pady=5, padx=20)

tipo_label = ctk.CTkLabel(frame_inputs, text="Tipo de Consulta:", anchor="w")
tipo_label.pack(fill="x", anchor="w", padx=20)
opcao_tipo = ctk.CTkComboBox(frame_inputs, values=["Campanha", "Gateway", "Healthscore"])
opcao_tipo.pack(fill="x", pady=5, padx=20)

consultar_botao = ctk.CTkButton(janela, text="Exportar", command=processar_consulta)
consultar_botao.pack(pady=10)

resultado_label = ctk.CTkLabel(janela, text="")
resultado_label.pack(pady=5)

janela.mainloop()
