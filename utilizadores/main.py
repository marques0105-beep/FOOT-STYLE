from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os

app = Flask(__name__)

# Chave secreta utilizada para assinar os tokens JWT
SECRET_KEY = os.environ.get("SECRET_KEY", "chave-temporaria-desenvolvimento")


# Base de dados simulada
# Mais tarde vamos substituir por uma base de dados real
utilizadores = []

# Contador de IDs
contador_id = 1


# ROTA PARA REGISTAR UM UTILIZADOR
@app.post("/utilizadores/registar")
def registar_utilizador():

    global contador_id

    dados = request.get_json(silent=True) or {}

    nome = dados.get("nome")
    email = dados.get("email")
    password = dados.get("password")

    # Verificar se os campos foram preenchidos
    if not nome or not email or not password:
        return jsonify({
            "erro": "Todos os campos são obrigatórios"
        }), 400

    # Verificar se o email já existe
    for utilizador in utilizadores:

        if utilizador["email"] == email:
            return jsonify({
                "erro": "Este email já está registado"
            }), 409

    # Criar o utilizador
    novo_utilizador = {
        "id": contador_id,
        "nome": nome,
        "email": email,
        "password": generate_password_hash(password)
    }

    utilizadores.append(novo_utilizador)

    contador_id += 1

    return jsonify({
        "mensagem": "Utilizador registado com sucesso",
        "id": novo_utilizador["id"],
        "nome": novo_utilizador["nome"],
        "email": novo_utilizador["email"]
    }), 201


# ROTA PARA LOGIN
@app.post("/utilizadores/login")
def login():

    dados = request.get_json(silent=True) or {}

    email = dados.get("email")
    password = dados.get("password")

    if not email or not password:
        return jsonify({
            "erro": "Email e password são obrigatórios"
        }), 400

    # Procurar o utilizador
    utilizador = next(
        (u for u in utilizadores if u["email"] == email),
        None
    )

    # Verificar se o utilizador existe e se a password está correta
    if not utilizador or not check_password_hash(
        utilizador["password"], password
    ):
        return jsonify({
            "erro": "Email ou password incorretos"
        }), 401

    # Criar token JWT
    token = jwt.encode(
        {
            "id": utilizador["id"],
            "email": utilizador["email"],
            "exp": datetime.datetime.now(datetime.timezone.utc)
                   + datetime.timedelta(hours=2)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({
        "mensagem": "Login efetuado com sucesso",
        "token": token
    }), 200


# ROTA PARA CONSULTAR O PERFIL
@app.get("/utilizadores/perfil")
def consultar_perfil():

    # Obter o token enviado pelo cliente
    cabecalho = request.headers.get("Authorization")

    if not cabecalho or not cabecalho.startswith("Bearer "):
        return jsonify({
            "erro": "Token de autenticação não fornecido"
        }), 401

    token = cabecalho.split(" ", 1)[1]

    try:

        # Verificar e descodificar o token
        dados_token = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        utilizador = next(
            (u for u in utilizadores if u["id"] == dados_token["id"]),
            None
        )

        if not utilizador:
            return jsonify({
                "erro": "Utilizador não encontrado"
            }), 404

        return jsonify({
            "id": utilizador["id"],
            "nome": utilizador["nome"],
            "email": utilizador["email"]
        }), 200

    except jwt.ExpiredSignatureError:

        return jsonify({
            "erro": "Token expirado"
        }), 401

    except jwt.InvalidTokenError:

        return jsonify({
            "erro": "Token inválido"
        }), 401


# Iniciar servidor Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
