from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from dao.servico_dao import ServicoDAO
bp=Blueprint("servicos",__name__,url_prefix="/api/servicos"); dao=ServicoDAO()
def valid(d):
    try: preco=float(d.get("preco"))
    except (TypeError,ValueError): return None
    nome=str(d.get("nome","")).strip()
    if not nome or preco<0:return None
    return {"nome":nome,"categoria":d.get("categoria"),"descricao":d.get("descricao"),"preco":preco,"ativo":bool(d.get("ativo",True))}
@bp.get("")
@jwt_required()
def listar():return jsonify(dao.listar(int(get_jwt_identity()))),200
@bp.get("/<int:sid>")
@jwt_required()
def buscar(sid):
    x=dao.buscar(int(get_jwt_identity()),sid);return (jsonify(x),200) if x else (jsonify({"erro":"Item não encontrado."}),404)
@bp.post("")
@jwt_required()
def criar():
    d=valid(request.get_json(silent=True) or {})
    if not d:return jsonify({"erro":"Nome e preço válido são obrigatórios."}),400
    return jsonify({"mensagem":"Item cadastrado.","id":dao.criar(int(get_jwt_identity()),d)}),201
@bp.put("/<int:sid>")
@jwt_required()
def atualizar(sid):
    d=valid(request.get_json(silent=True) or {})
    if not d:return jsonify({"erro":"Nome e preço válido são obrigatórios."}),400
    ok=dao.atualizar(int(get_jwt_identity()),sid,d);return (jsonify({"mensagem":"Item atualizado."}),200) if ok else (jsonify({"erro":"Item não encontrado."}),404)
@bp.delete("/<int:sid>")
@jwt_required()
def excluir(sid):
    try: ok=dao.excluir(int(get_jwt_identity()),sid)
    except Exception:return jsonify({"erro":"Não é possível excluir um item que já foi usado em orçamento."}),409
    return (jsonify({"mensagem":"Item excluído."}),200) if ok else (jsonify({"erro":"Item não encontrado."}),404)
