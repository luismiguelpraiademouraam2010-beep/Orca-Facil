from flask import Flask,jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from routes.auth_routes import bp as auth_bp
from routes.cliente_routes import bp as clientes_bp
from routes.servico_routes import bp as servicos_bp
from routes.orcamento_routes import bp as orcamentos_bp
from routes.empresa_routes import bp as empresa_bp

def create_app():
    app=Flask(__name__); app.config.from_object(Config)
    CORS(app,origins=Config.CORS_ORIGINS,allow_headers=["Content-Type","Authorization"],methods=["GET","POST","PUT","PATCH","DELETE","OPTIONS"])
    JWTManager(app)
    for bp in (auth_bp,clientes_bp,servicos_bp,orcamentos_bp,empresa_bp):app.register_blueprint(bp)
    @app.get("/")
    def home():return jsonify({"sistema":"OrçaFácil API","status":"online","versao":"1.0"})
    @app.get("/api/status")
    def status():return jsonify({"status":"online","mensagem":"API OrçaFácil funcionando."})
    @app.errorhandler(404)
    def not_found(_):return jsonify({"erro":"Rota não encontrada."}),404
    @app.errorhandler(500)
    def internal(_):return jsonify({"erro":"Erro interno do servidor."}),500
    return app
app=create_app()
if __name__=="__main__":app.run(host="127.0.0.1",port=5000,debug=True)
