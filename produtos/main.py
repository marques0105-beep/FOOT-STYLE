# Importa as ferramentas necessárias do Flask:
from flask import Flask, jsonify, render_template

# Inicializa a aplicação Flask
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

# Rota API para listar todos os produtos em formato JSON
@app.get("/produtos")
def listar_produtos():
    return jsonify(produtos)

# Rota API para obter os detalhes de um único produto específico através do seu ID
@app.get("/produtos/<int:produto_id>")
def obter_produto(produto_id):
    # Procura na lista o produto que tem o ID correspondente
    produto = next((p for p in produtos if p["id"] == produto_id), None)

# Se o produto não existir, retorna um erro 404
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify(produto)

# Rota para a página principal (Interface Web simples)
@app.get("/")
def pagina_inicial():
    # Renderiza o ficheiro HTML e envia a lista de produtos para lá
    return render_template("index.html", produtos=produtos)

# Inicia o servidor Flask quando o script é executado diretamente
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)