# Exportador de Dados via API  

Este é um aplicativo de interface gráfica para exportação de dados via requisições HTTP a partir de uma API gerenciada pelo **N8N**. Ele permite que o usuário consulte dados específicos de um banco de dados e salve os resultados em um arquivo CSV.  

## 🚀 Como Funciona  

1. O usuário insere **datas, IDs de empresas e o tipo de consulta** na interface.  
2. O aplicativo faz uma requisição para um endpoint do **N8N**, que atua como intermediário entre a aplicação e o banco de dados.  
3. O **N8N** processa a requisição, acessa o banco de dados e retorna os dados no formato JSON.  
4. O aplicativo recebe os dados e permite a exportação para um **arquivo CSV**.  

## 🛠️ O que é o N8N?  

[N8N](https://n8n.io/) é uma plataforma de automação de fluxo de trabalho **low-code** e **open-source**, que permite conectar APIs, bancos de dados e diversas ferramentas sem necessidade de programação complexa.  

No contexto deste projeto, o **N8N**:  
- Recebe as requisições do aplicativo via **webhook**  
- Consulta o banco de dados conforme os filtros fornecidos (datas, IDs, tipo de consulta)  
- Processa e formata os dados  
- Retorna a resposta para o aplicativo  

## 🛠️ Tecnologias Utilizadas  

- **Python**  
- **CustomTkinter** (Interface gráfica)  
- **Requests** (Requisições HTTP)  
- **Pandas** (Manipulação de dados)  
- **Pillow** (Imagens)  
- **dotenv** (Carregamento de variáveis de ambiente)  
- **N8N** (Orquestração e conexão com banco de dados)  

## 📦 Instalação  

1. Clone o repositório:  

   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio

2. Crie um ambiente virtual e ative:  

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS  
   venv\Scripts\activate  # Windows  

3. Instale as dependências:  

   ```bash
   pip install -r requirements.txt

4. Configure as variáveis de ambiente no arquivo .env:  

   ```bash
   URL_HEALTH=https://seu-n8n.com/health
   WEBHOOK_URL=https://seu-n8n.com/webhook

## 🔍 Como Usar  
1. Execute o script:  

   ```bash
   python main.py

2. Insira as informações necessárias:

    - Data de Início e Fim no formato AAAA-MM-DD

    - IDs das Empresas (separados por vírgulas)

    - Tipo de Consulta desejado

3. Clique no botão "Exportar" para obter os dados.

4. Escolha um local para salvar o arquivo CSV.

## 🛠️ Possíveis Erros e Soluções  

| Erro | Solução |  
|------|---------|  
| **Permissão negada ao acessar API** | Verifique se a URL `URL_HEALTH` está correta e acessível |  
| **Erro ao processar resposta do servidor** | Certifique-se de que a API do **N8N** está retornando um JSON válido |  
| **IDs inválidos** | Digite IDs separados por vírgulas, sem espaços extras |  
| **Não foi possível salvar o CSV** | Escolha um caminho válido e verifique as permissões de escrita |  