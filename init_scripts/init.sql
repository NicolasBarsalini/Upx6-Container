DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_database WHERE datname = 'estufa'
   ) THEN
      CREATE DATABASE estufa;
   END IF;
END
$$;

\c estufa

SET timezone = 'America/Sao_Paulo'; -- Ajuste para o seu fuso horário

CREATE TABLE IF NOT EXISTS estufa_data (
    id SERIAL PRIMARY KEY,
    temperature NUMERIC NOT NULL,
    humidity NUMERIC NOT NULL,
    fan_speed NUMERIC NOT NULL,
    light_status BOOLEAN NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP UNIQUE
);

-- Criar a função para validar o tempo
CREATE OR REPLACE FUNCTION validate_time_difference()
RETURNS TRIGGER AS $$
DECLARE
    last_timestamp TIMESTAMP;
BEGIN
    -- Verificar o último timestamp
    SELECT timestamp
    INTO last_timestamp
    FROM estufa_data
    ORDER BY timestamp DESC
    LIMIT 1;

    -- Verificar diferença mínima de 1 minuto entre timestamps
    IF last_timestamp IS NOT NULL AND (NEW.timestamp - last_timestamp) < interval '1 minute' THEN
        RAISE EXCEPTION 'Cannot insert data: timestamp too close to the last entry.';
    END IF;

    -- Permitir a inserção se todas as condições forem atendidas
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Remover trigger existente, se houver
DROP TRIGGER IF EXISTS trigger_validate_time_difference ON estufa_data;

-- Criar nova trigger
CREATE TRIGGER trigger_validate_time_difference
BEFORE INSERT ON estufa_data
FOR EACH ROW
EXECUTE FUNCTION validate_time_difference();