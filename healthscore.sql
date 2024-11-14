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
            AND companies.id IN ({ids})
        ORDER BY companies.id;