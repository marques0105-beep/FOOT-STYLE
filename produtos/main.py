from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Catálogo simulado com marcas, modelos, tamanhos e stock
produtos = [
    {
        "id": 1,
        "marca": "Nike",
        "modelo": "Air Force 1",
        "preco": 99.99,
        "stocks": {
            "40": 5,
            "41": 10,
            "42": 2
        }
    },
    {
        "id": 2,
        "marca": "Adidas",
        "modelo": "Superstar",
        "preco": 89.99,
        "stocks": {
            "39": 4,
            "41": 8,
            "42": 6
        }
    }
]

@app.get("/produtos")
def listar_produtos():
    return jsonify(produtos)

@app.get("/produtos/<int:produto_id>")
def obter_produto(produto_id):
    produto = next((p for p in produtos if p["id"] == produto_id), None)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify(produto)

@app.get("/")
def pagina_inicial():
    return render_template("index.html", produtos=produtos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)