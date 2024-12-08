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