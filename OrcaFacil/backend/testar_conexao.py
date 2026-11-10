from config.database import obter_conexao

try:
    conexao = obter_conexao()
    print("Conexão com banco_projeto realizada com sucesso.")
    conexao.close()
except Exception as erro:
    print(f"Falha na conexão: {erro}")
