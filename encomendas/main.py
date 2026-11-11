from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.get("/encomendas")
def consultar_encomenda():
    resposta = requests.get( "http://api-produtos:5000/produtos" )
    produtos = resposta.json()
    return produtos 

#usamos a biblioteca request para fazer os pedidos (conexão carlho fds)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
