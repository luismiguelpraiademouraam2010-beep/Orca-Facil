import os
from datetime import date
from functools import wraps

import mysql.connector
from flask import Flask, jsonify, request, session, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app = Flask(__name__, static_folder=ROOT, static_url_path="")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "troque-esta-chave-antes-de-publicar")
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")

# O próprio Flask serve o frontend e a API na mesma origem.
CORS(app, supports_credentials=True)

def db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "orcafacil"),
    )

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"erro": "Faça login para continuar."}), 401
        return fn(*args, **kwargs)
    return wrapper

@app.get("/")
def home():
    return send_from_directory(ROOT, "index.html")

@app.get("/api/health")
def health():
    try:
        con = db()
        con.close()
        return jsonify({"status": "ok", "database": "connected"})
    except mysql.connector.Error as exc:
        return jsonify({"status": "error", "message": str(exc)}), 503

@app.post("/api/register")
def register():
    data = request.get_json(silent=True) or {}
    nome = str(data.get("nome", "")).strip()
    empresa = str(data.get("empresa", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    senha = str(data.get("senha", ""))
    if not all([nome, empresa, email, senha]) or len(senha) < 6:
        return jsonify({"erro": "Informe todos os campos e uma senha com pelo menos 6 caracteres."}), 400
    con = db()
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO usuarios (nome, empresa, email, senha_hash) VALUES (%s,%s,%s,%s)",
                    (nome, empresa, email, generate_password_hash(senha)))
        con.commit()
        session["user_id"] = cur.lastrowid
        session["user_name"] = nome
        return jsonify({"mensagem": "Conta criada com sucesso.", "usuario": {"nome": nome, "email": email}}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"erro": "Este e-mail já possui cadastro."}), 409
    finally:
        cur.close()
        con.close()

@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    senha = str(data.get("senha", ""))
    con = db()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT id,nome,email,senha_hash FROM usuarios WHERE email=%s", (email,))
    user = cur.fetchone()
    cur.close()
    con.close()
    if not user or not check_password_hash(user["senha_hash"], senha):
        return jsonify({"erro": "E-mail ou senha incorretos."}), 401
    session["user_id"] = user["id"]
    session["user_name"] = user["nome"]
    return jsonify({"usuario": {"nome": user["nome"], "email": user["email"]}})

@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify({"mensagem": "Sessão encerrada."})

# As listas do painel são persistidas nas tabelas relacionais por usuário.
RESOURCE_CONFIG = {
    "clients": ("clientes", ["nome", "email", "telefone", "empresa"]),
    "services": ("servicos", ["nome", "categoria", "descricao", "preco"]),
    "budgets": ("orcamentos", ["cliente", "descricao", "data", "validade", "status", "total"]),
}

@app.get("/api/data/<resource>")
@login_required
def get_data(resource):
    if resource == "company":
        table, cols = "empresas", ["nome", "cnpj", "email", "telefone", "endereco", "descricao"]
        con = db(); cur = con.cursor(dictionary=True)
        cur.execute("SELECT nome,cnpj,email,telefone,endereco,descricao FROM empresas WHERE usuario_id=%s", (session["user_id"],))
        row = cur.fetchone() or {}
        cur.close(); con.close()
        return jsonify(row)
    if resource not in RESOURCE_CONFIG:
        return jsonify({"erro": "Recurso inválido."}), 404
    table, cols = RESOURCE_CONFIG[resource]
    con = db(); cur = con.cursor(dictionary=True)
    cur.execute(f"SELECT id,{','.join(cols)} FROM {table} WHERE usuario_id=%s ORDER BY id", (session["user_id"],))
    rows = cur.fetchall()
    cur.close(); con.close()
    for row in rows:
        if resource == "budgets":
            row["id"] = str(row["id"])
            row["data"] = str(row["data"])
            row["validade"] = str(row["validade"]) if row["validade"] else ""
        if resource == "services":
            row["preco"] = float(row["preco"])
    return jsonify(rows)

@app.put("/api/data/<resource>")
@login_required
def put_data(resource):
    data = request.get_json(silent=True)
    if resource == "company":
        data = data or {}
        con = db(); cur = con.cursor()
        cur.execute("""INSERT INTO empresas (usuario_id,nome,cnpj,email,telefone,endereco,descricao)
          VALUES (%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE
          nome=VALUES(nome),cnpj=VALUES(cnpj),email=VALUES(email),telefone=VALUES(telefone),
          endereco=VALUES(endereco),descricao=VALUES(descricao)""",
          (session["user_id"], data.get("nome"), data.get("cnpj"), data.get("email"),
           data.get("telefone"), data.get("endereco"), data.get("descricao")))
        con.commit(); cur.close(); con.close()
        return jsonify({"mensagem": "Empresa salva."})
    if resource not in RESOURCE_CONFIG or not isinstance(data, list):
        return jsonify({"erro": "Dados inválidos."}), 400
    table, cols = RESOURCE_CONFIG[resource]
    con = db(); cur = con.cursor()
    cur.execute(f"DELETE FROM {table} WHERE usuario_id=%s", (session["user_id"],))
    for item in data:
        values = [item.get(c) for c in cols]
        if resource == "budgets":
            values[2] = values[2] or date.today().isoformat()
            values[3] = values[3] or None
        placeholders = ",".join(["%s"] * (len(cols) + 1))
        cur.execute(f"INSERT INTO {table} (usuario_id,{','.join(cols)}) VALUES ({placeholders})",
                    [session["user_id"], *values])
    con.commit(); cur.close(); con.close()
    return jsonify({"mensagem": "Dados sincronizados."})

@app.get("/<path:path>")
def static_files(path):
    return send_from_directory(ROOT, path)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
