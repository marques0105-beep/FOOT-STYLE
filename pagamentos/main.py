from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista simulada de pagamentos
# Mais tarde podemos substituir por uma base de dados
pagamentos = []

# Contador de IDs
contador_id = 1


# ROTA PARA PROCESSAR UM PAGAMENTO
@app.post("/pagamentos")
def processar_pagamento():

    global contador_id

    dados = request.get_json(silent=True) or {}

    encomenda_id = dados.get("encomenda_id")
    valor = dados.get("valor")
    resultado = dados.get("resultado", "aprovado")

    # Verificar os campos obrigatórios
    if encomenda_id is None or valor is None:
        return jsonify({
            "erro": "O ID da encomenda e o valor são obrigatórios"
        }), 400

    # Validar o valor
    try:
        valor = float(valor)
    except (ValueError, TypeError):
        return jsonify({
            "erro": "O valor do pagamento é inválido"
        }), 400

    if valor <= 0:
        return jsonify({
            "erro": "O valor deve ser superior a zero"
        }), 400

    # Verificar o resultado da simulação
    if resultado not in ["aprovado", "recusado"]:
        return jsonify({
            "erro": "Resultado deve ser aprovado ou recusado"
        }), 400

    # Verificar se já existe um pagamento para esta encomenda
    pagamento_existente = next(
        (
            p for p in pagamentos
            if p["encomenda_id"] == encomenda_id
        ),
        None
    )

    if pagamento_existente:
        return jsonify({
            "erro": "Esta encomenda já tem um pagamento registado"
        }), 409

    # Criar o pagamento
    novo_pagamento = {
        "id": contador_id,
        "encomenda_id": encomenda_id,
        "valor": round(valor, 2),
        "estado": resultado
    }

    pagamentos.append(novo_pagamento)

    contador_id += 1

    return jsonify({
        "mensagem": "Pagamento processado",
        "pagamento": novo_pagamento
    }), 201


# ROTA PARA CONSULTAR UM PAGAMENTO
@app.get("/pagamentos/<int:pagamento_id>")
def consultar_pagamento(pagamento_id):

    pagamento = next(
        (
            p for p in pagamentos
            if p["id"] == pagamento_id
        ),
        None
    )

    if not pagamento:
        return jsonify({
            "erro": "Pagamento não encontrado"
        }), 404

    return jsonify(pagamento), 200


# ROTA PARA CONSULTAR TODOS OS PAGAMENTOS
@app.get("/pagamentos")
def listar_pagamentos():

    return jsonify(pagamentos), 200


# Iniciar servidor Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
