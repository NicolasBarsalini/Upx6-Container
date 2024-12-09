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

CREATE TABLE IF NOT EXISTS estufa_data (
    id SERIAL PRIMARY KEY,
    temperature NUMERIC NOT NULL,
    humidity NUMERIC NOT NULL,
    fan_speed NUMERIC NOT NULL,
    light_status BOOLEAN NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar a função para validar o tempo
CREATE OR REPLACE FUNCTION validate_time_difference()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar o último timestamp na tabela
    IF EXISTS (SELECT 1 FROM estufa_data WHERE (NOW() - timestamp) < interval '5 minutes') THEN
        RAISE EXCEPTION 'Cannot insert data: less than 5 minutes since the last entry.';
    END IF;

    -- Permitir a inserção se a condição for atendida
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Criar a trigger que chama a função antes da inserção
CREATE TRIGGER trigger_validate_time_difference
BEFORE INSERT ON estufa_data
FOR EACH ROW
EXECUTE FUNCTION validate_time_difference();