from datetime import date
from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from dao.orcamento_dao import OrcamentoDAO
bp=Blueprint("orcamentos",__name__,url_prefix="/api/orcamentos"); dao=OrcamentoDAO()
STATUS={"Pendente","Aprovado","Rejeitado"}
@bp.get("")
@jwt_required()
def listar():return jsonify(dao.listar(int(get_jwt_identity()))),200
@bp.get("/<int:oid>")
@jwt_required()
def buscar(oid):
    x=dao.buscar(int(get_jwt_identity()),oid);return (jsonify(x),200) if x else (jsonify({"erro":"Orçamento não encontrado."}),404)
@bp.post("")
@jwt_required()
def criar():
    d=request.get_json(silent=True) or {}
    try:
        payload={"cliente_id":int(d.get("cliente_id")),"descricao":str(d.get("descricao","")).strip() or "Orçamento","data_orcamento":date.today(),"validade":date.fromisoformat(d["validade"]) if d.get("validade") else None,"desconto":float(d.get("desconto",0))}
        itens=d.get("itens",[])
        oid=dao.criar(int(get_jwt_identity()),payload,itens)
        return jsonify({"mensagem":"Orçamento criado.","id":oid}),201
    except (TypeError,ValueError,KeyError) as e:return jsonify({"erro":str(e) or "Dados inválidos."}),400
@bp.patch("/<int:oid>/status")
@jwt_required()
def status(oid):
    s=(request.get_json(silent=True) or {}).get("status")
    if s not in STATUS:return jsonify({"erro":"Status deve ser Pendente, Aprovado ou Rejeitado."}),400
    ok=dao.atualizar_status(int(get_jwt_identity()),oid,s);return (jsonify({"mensagem":"Status atualizado."}),200) if ok else (jsonify({"erro":"Orçamento não encontrado."}),404)
@bp.delete("/<int:oid>")
@jwt_required()
def excluir(oid):
    ok=dao.excluir(int(get_jwt_identity()),oid);return (jsonify({"mensagem":"Orçamento excluído."}),200) if ok else (jsonify({"erro":"Orçamento não encontrado."}),404)
@bp.get("/relatorio/resumo")
@jwt_required()
def resumo():return jsonify(dao.resumo(int(get_jwt_identity()))),200
