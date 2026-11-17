from flask import Blueprint,request,jsonify
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from werkzeug.security import generate_password_hash,check_password_hash
from dao.usuario_dao import UsuarioDAO
bp=Blueprint("auth",__name__,url_prefix="/api/auth"); dao=UsuarioDAO()
@bp.post("/register")
def register():
    d=request.get_json(silent=True) or {}; nome=str(d.get("nome","")).strip(); email=str(d.get("email","")).strip().lower(); senha=str(d.get("senha",""))
    if not nome or not email or "@" not in email or len(senha)<8: return jsonify({"erro":"Informe nome, e-mail válido e senha com pelo menos 8 caracteres."}),400
    if dao.buscar_por_email(email): return jsonify({"erro":"E-mail já cadastrado."}),409
    uid=dao.criar(nome,email,generate_password_hash(senha)); token=create_access_token(identity=str(uid))
    return jsonify({"mensagem":"Conta criada.","access_token":token,"usuario":{"id":uid,"nome":nome,"email":email}}),201
@bp.post("/login")
def login():
    d=request.get_json(silent=True) or {}; u=dao.buscar_por_email(str(d.get("email","")).strip().lower())
    if not u or not check_password_hash(u["senha_hash"],str(d.get("senha",""))): return jsonify({"erro":"E-mail ou senha incorretos."}),401
    return jsonify({"access_token":create_access_token(identity=str(u["id"])),"usuario":{"id":u["id"],"nome":u["nome"],"email":u["email"]}}),200
@bp.get("/me")
@jwt_required()
def me():
    u=dao.buscar_por_id(int(get_jwt_identity()))
    return (jsonify({"usuario":u}),200) if u else (jsonify({"erro":"Usuário não encontrado."}),404)
