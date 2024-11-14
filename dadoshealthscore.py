import pandas as pd
import mysql.connector
import time

# Configuração de conexão ao banco de dados
db_username = 'suporte'
db_password = 'LewSG907$yX5'
db_host = 'mysql-zapisp-prod.cayxp5jpjfif.us-east-1.rds.amazonaws.com'
db_database = 'zapisp'

GREEN_COLOR = "\033[92m"
RED_COLOR = "\033[91m"
RESET_COLOR = "\033[0m"
BLUE_COLOR = '\033[94m'

inicio = '2024-04-01'
fim = '2024-04-30'


# Lista de IDs de empresas
ids = [626, 587, 580, 451, 435, 403, 401, 400, 174, 104, 76, 61, 45, 33, 32, 28, 13, 21, 100, 101, 103, 105, 106, 107, 108, 109, 111, 112, 114, 115, 116, 118, 120, 121, 126, 129, 132, 133, 136, 141, 142, 143, 146, 147, 148, 151, 152, 153, 154, 155, 156, 164, 167, 168, 173, 175, 176, 182, 184, 185, 186, 188, 193, 197, 203, 204, 206, 207, 208, 209, 212, 215, 216, 217, 218, 222, 223, 227, 230, 231, 233, 235, 237, 238, 240, 242, 245, 246, 250, 251, 253, 256, 257, 261, 264, 269, 272, 276, 277, 279, 280, 281, 283, 284, 289, 293, 294, 297, 298, 299, 300, 301, 304, 305, 307, 308, 310, 311, 312, 313, 317, 320, 322, 323, 324, 325, 326, 329, 332, 333, 334, 335, 338, 341, 342, 344, 345, 347, 349, 350, 351, 352, 353, 357, 377, 379, 38, 380, 382, 386, 39, 390, 392, 395, 407, 408, 409, 417, 418, 42, 421, 423, 424, 427, 431, 433, 440, 443, 444, 447, 448, 449, 452, 453, 455, 458, 459, 465, 470, 471, 475, 477, 484, 487, 488, 489, 49, 490, 491, 494, 495, 496, 497, 498, 499, 500, 501, 503, 504, 507, 51, 512, 513, 515, 516, 52, 524, 526, 527, 530, 531, 532, 535, 540, 543, 545, 547, 548, 550, 552, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 571, 572, 573, 574, 589, 59, 593, 594, 595, 60, 600, 601, 602, 603, 604, 605, 606, 613, 65, 67, 69, 73, 74, 75, 78, 80, 82, 85, 88, 89, 90, 91, 92, 93, 95, 97, 98]

# Conexão com o banco e consulta por ID em lotes
try:
    connection = mysql.connector.connect(
        host=db_host,
        database=db_database,
        user=db_username,
        password=db_password # Habilita a recuperação da chave pública
    )    
    cursor = connection.cursor(dictionary=True)

    # DataFrame vazio para armazenar resultados
    df_resultado = pd.DataFrame()

    # Iterar sobre IDs em lotes (ajuste o tamanho do lote conforme necessário)
    lote_tamanho = 10
    for i in range(0, len(ids), lote_tamanho):
        lote_ids = ids[i:i + lote_tamanho]

        # Construir a query para o lote atual
        query = f"""
        SELECT 
            companies.id, 
            companies.nome_fantasia, 
            (SELECT p.nome
            FROM planos p 
            WHERE p.id = companies.plano_id
            ) AS plano,
            (SELECT COUNT(*) 
            FROM clients c 
            WHERE c.client_usuario_id = companies.id
            AND c.created_at >= '{inicio}' 
            AND c.created_at <= '{fim}'
            AND c.client_status = 1
            ) AS qtd_clientes,
            (SELECT COUNT(*) 
            FROM nps n
            WHERE n.survey_usuario_id = companies.id
            AND n.created_at >= '{inicio}' 
            AND n.created_at <= '{fim}'
            ) AS qtd_nps,
            (SELECT COUNT(*) 
            FROM after_service as2 
            WHERE as2.after_service_usuario_id = companies.id
            AND as2.created_at >= '{inicio}' 
            AND as2.created_at <= '{fim}'
            ) AS qtd_pa,
            (SELECT COUNT(*) 
            FROM leads l 
            WHERE l.lead_usuario_id = companies.id 
            AND l.lead_origin = 'marketing'
            AND l.lead_outcome = 0
            AND l.created_at >= '{inicio}' 
            AND l.created_at <= '{fim}'
            ) AS qtd_leads_ganho_marketing
        FROM companies
        WHERE companies.deleted_at IS NULL
            AND companies.id IN ({', '.join(map(str, lote_ids))})
        ORDER BY companies.id;
        """

        cursor.execute(query)
        resultados = cursor.fetchall()
        
        # Adicionar resultados ao DataFrame
        df_resultado = pd.concat([df_resultado, pd.DataFrame(resultados)], ignore_index=True)
        
        print(f"{GREEN_COLOR}Lote de IDs {lote_ids} processado com sucesso.{RESET_COLOR}")
        
        # Pausa opcional para evitar sobrecarregar o banco
        time.sleep(0.5)

    # Exportar para CSV
    df_resultado.to_csv(f'dados_healthscore_{inicio}_{fim}.csv', index=False)
    print(f"{GREEN_COLOR}Dados exportados para 'dados_companies_mysql.csv' com sucesso.{RESET_COLOR}")

except mysql.connector.Error as error:
    print(f"{RED_COLOR}Erro ao conectar ao banco de dados: {error}{RESET_COLOR}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()

