 SELECT
            c2.id,
            c2.nome_fantasia, 
            COUNT(*) AS qtd_campanhas
        FROM
            campaigns_history ch
        INNER JOIN campaigns c 
            ON ch.id_campaign = c.campaign_id
        INNER JOIN companies c2 
            ON c2.id = c.campaign_usuario_id
        WHERE ch.created_at >= '{inicio}' 
            AND ch.created_at <= '{fim}'
            AND c2.deleted_at IS NULL 
            AND c2.id IN ({ids})
        GROUP BY
            c2.id, c2.nome_fantasia
        ORDER BY
            c2.nome_fantasia;