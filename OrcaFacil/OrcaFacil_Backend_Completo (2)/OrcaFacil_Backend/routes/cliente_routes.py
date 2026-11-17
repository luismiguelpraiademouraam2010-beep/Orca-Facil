from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from dao.cliente_dao import ClienteDAO
bp=Blueprint("clientes",__name__,url_prefix="/api/clientes"); dao=ClienteDAO()
def valid(d):
    nome=str(d.get("nome","")).strip(); email=str(d.get("email","")).strip()
    if not nome or "@" not in email: return None
    return {"nome":nome,"email":email,"telefone":d.get("telefone"),"empresa":d.get("empresa")}
@bp.get("")
@jwt_required()
def listar(): return jsonify(dao.listar(int(get_jwt_identity()))),200
@bp.get("/<int:cid>")
@jwt_required()
def buscar(cid):
    x=dao.buscar(int(get_jwt_identity()),cid); return (jsonify(x),200) if x else (jsonify({"erro":"Cliente não encontrado."}),404)
@bp.post("")
@jwt_required()
def criar():
    d=valid(request.get_json(silent=True) or {})
    if not d:return jsonify({"erro":"Nome e e-mail válido são obrigatórios."}),400
    return jsonify({"mensagem":"Cliente cadastrado.","id":dao.criar(int(get_jwt_identity()),d)}),201
@bp.put("/<int:cid>")
@jwt_required()
def atualizar(cid):
    d=valid(request.get_json(silent=True) or {})
    if not d:return jsonify({"erro":"Nome e e-mail válido são obrigatórios."}),400
    ok=dao.atualizar(int(get_jwt_identity()),cid,d); return (jsonify({"mensagem":"Cliente atualizado."}),200) if ok else (jsonify({"erro":"Cliente não encontrado."}),404)
@bp.delete("/<int:cid>")
@jwt_required()
def excluir(cid):
    ok=dao.excluir(int(get_jwt_identity()),cid); return (jsonify({"mensagem":"Cliente excluído."}),200) if ok else (jsonify({"erro":"Cliente não encontrado ou vinculado a orçamento."}),404)
