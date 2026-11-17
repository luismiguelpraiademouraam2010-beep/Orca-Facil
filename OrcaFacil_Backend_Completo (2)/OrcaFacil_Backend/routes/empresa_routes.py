from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from dao.empresa_dao import EmpresaDAO
bp=Blueprint("empresa",__name__,url_prefix="/api/empresa");dao=EmpresaDAO()
@bp.get("")
@jwt_required()
def buscar():return jsonify(dao.buscar(int(get_jwt_identity())) or {}),200
@bp.put("")
@jwt_required()
def salvar():
    d=request.get_json(silent=True) or {}
    if not str(d.get("nome","")).strip():return jsonify({"erro":"Nome da empresa obrigatório."}),400
    dao.salvar(int(get_jwt_identity()),d);return jsonify({"mensagem":"Empresa atualizada."}),200
