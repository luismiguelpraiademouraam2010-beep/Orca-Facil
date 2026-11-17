from database.connection import get_connection
class EmpresaDAO:
    def buscar(self,uid):
        c=get_connection()
        try:
            q=c.cursor(dictionary=True); q.execute("SELECT nome,cnpj,email,telefone,endereco,descricao FROM empresas WHERE usuario_id=%s",(uid,)); return q.fetchone()
        finally: c.close()
    def salvar(self,uid,d):
        c=get_connection()
        try:
            q=c.cursor(); q.execute("""UPDATE empresas SET nome=%s,cnpj=%s,email=%s,telefone=%s,endereco=%s,descricao=%s
                                       WHERE usuario_id=%s""",(d.get('nome'),d.get('cnpj'),d.get('email'),d.get('telefone'),d.get('endereco'),d.get('descricao'),uid)); c.commit()
        except Exception: c.rollback(); raise
        finally: c.close()
