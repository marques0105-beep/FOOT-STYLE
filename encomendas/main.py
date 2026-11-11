from flask import Flask, jsonify
import requests

# Inicializa a aplicação Flask
app = Flask(__name__)


# Rota para consultar os produtos através do microserviço Produtos
@app.get("/encomendas")
def consultar_encomenda():

    try:

        resposta = requests.get(
            "http://api-produtos:5000/produtos",
            timeout=5
        )

        resposta.raise_for_status()

        produtos = resposta.json()

        return jsonify(produtos)

    except requests.exceptions.RequestException:

        return jsonify({
            "erro": "Não foi possível comunicar com o microserviço Produtos"
        }), 503


# Inicia o servidor Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0")
