import json
import time
import zenoh
from flask_cors import CORS
from flask import Flask, Response, stream_with_context, request, jsonify

app = Flask(__name__)
CORS(app)

# Configuração do Zenoh
session = zenoh.open(zenoh.Config())
subscribe_key = 'demo/example/zenoh_sub'
publish_key = 'demo/example/zenoh_pub'

# Variáveis globais
latest_data = {"temperature": None, "humidity": None, "fanSpeed": None, "lightStatus": None}

seted_data = {"temperature": None, "humidity": None, "fanSpeed": None}

# Declare o assinante Zenoh
def listener(sample):
    global latest_data
    try:
        # Decodifique e atualize os dados mais recentes
        payload = bytes(sample.payload).decode('utf-8')
        print(f"Received: {payload}")
        latest_data = json.loads(payload)
    except Exception as e:
        print(f"Error processing sample: {e}")


session.declare_subscriber(subscribe_key, listener)

# Declare o publicador Zenoh
publisher = session.declare_publisher(publish_key)

# Rota para SSE
@app.route('/events', methods=['GET'])
def events():
    def generate():
        while True:
            # Envia os dados mais recentes para os clientes SSE
            yield f"data: {json.dumps(latest_data)}\n\n"
            time.sleep(1)
    return Response(stream_with_context(generate()), content_type='text/event-stream')

# Rota para atualizar dados e publicar no Zenoh
@app.route('/update', methods=['POST'])
def update_data():
    global seted_data
    data = request.json
    if data:
        # Atualize os dados configurados
        seted_data.update(data)
        print(f"Updated data: {seted_data}")

        # Publique os dados atualizados no canal Zenoh
        try:
            payload = json.dumps(seted_data)  # Converta os dados em JSON
            publisher.put(payload)           # Publique no canal Zenoh
            print(f"Published to Zenoh: {payload}")
            return jsonify({"status": "success", "published": seted_data}), 200
        except Exception as e:
            print(f"Error publishing to Zenoh: {e}")
            return jsonify({"status": "error", "message": "Failed to publish"}), 500

    return jsonify({"status": "error", "message": "No data received"}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", threaded=True)
