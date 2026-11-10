from flask import Flask, jsonify
from config.database import obter_conexao

app = Flask(__name__)

@app.get("/api/status")
def status_sistema():
    try:
        conexao = obter_conexao()
        conexao.close()
        return jsonify({"api": "online", "banco_de_dados": "conectado"}), 200
    except Exception:
        return jsonify({"api": "online", "banco_de_dados": "indisponivel"}), 503

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
