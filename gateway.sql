
    SELECT
        c.id,
        c.nome_fantasia AS nome_empresa,
        COUNT(iqsm.id) AS quantidade_gateway
    FROM 
        instance_queue_scheduled iqs
    INNER JOIN 
        instance_queue_scheduled_messages iqsm 
        ON iqs.id = iqsm.instance_queue_scheduled_id 
    INNER JOIN 
        companies c  
        ON c.id = iqs.empresa_id  
    WHERE 
        iqs.nome LIKE '%Fila do Gateway%' 
        AND iqsm.status = 4
        AND iqsm.created_at >= '{inicio}' 
        AND iqsm.created_at <= '{fim}'
        AND c.id IN ({ids})
      GROUP BY 
        c.id
        ORDER BY
            c.nome_fantasia;

