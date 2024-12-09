from flask_cors import CORS
import psycopg2
from psycopg2 import sql
from flask import Flask, jsonify
import zenoh
import json

# Configurar Flask
app = Flask(__name__)
CORS(app)

# Configuração de banco de dados
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'estufa',
    'user': 'admin',
    'password': 'admin'
}

# Variáveis globais para conexão
cursor = None
connection = None


def connect_database(CONFIG):
    global cursor
    global connection
    try:
        connection = psycopg2.connect(**CONFIG)
        cursor = connection.cursor()
        print("Connected to the database!")
    except psycopg2.Error as e:
        print("Error connecting to the database! ", e)


def insert_information_into_database(data):
    global cursor
    global connection
    try:
        temperature = data.get("temperature")
        humidity = data.get("humidity")
        fan_speed = data.get("fanSpeed")
        light_status = data.get("lightStatus")
        insert_query = """
            INSERT INTO estufa_data (temperature, humidity, fan_speed, light_status)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(insert_query, (temperature,
                       humidity, fan_speed, light_status))

        connection.commit()
        print("Data inserted successfully!")

    except psycopg2.errors.RaiseException as e:
        print(f"Error inserting information into database: {e}")
        connection.rollback()

    except Exception as e:
        print(f"Error inserting information into database: {e}")
        connection.rollback()

def listener(sample):
    payload = bytes(sample.payload).decode('utf-8')
    print(f"Received: {payload}")
    data = json.loads(payload)
    insert_information_into_database(data)

# Rota para buscar os últimos dados
@app.route('/get_graph_data', methods=['GET'])
def get_graph_data():
    global cursor
    try:
        # Query para pegar todos os dados inseridos
        select_query = """
            SELECT *
            FROM estufa_data
            ORDER BY timestamp DESC;
        """
        cursor.execute(select_query)
        results = cursor.fetchall()  # Pega todos os registros

        if results:
            # Mapear todos os resultados para uma lista de JSONs
            response = [
                {
                    'id': row[0],
                    'temperature': row[1],
                    'humidity': row[2],
                    'fan_speed': row[3],
                    'light_status': row[4],
                    'timestamp': row[5].strftime("%Y-%m-%d %H:%M:%S")
                }
                for row in results
            ]
            return jsonify(response)
        else:
            return jsonify({"error": "No data available"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Conectar ao banco de dados
    connect_database(DB_CONFIG)

    # Configurar Zenoh
    KEY = 'demo/example/zenoh_sub'
    session = zenoh.open(zenoh.Config())
    sub = session.declare_subscriber(KEY, listener)

    # Iniciar o servidor Flask
    app.run(debug=True, host="0.0.0.0", threaded=True, port=7766)
