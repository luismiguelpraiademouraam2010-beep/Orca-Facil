from database.connection import get_connection
class ServicoDAO:
    def listar(self,uid):
        c=get_connection()
        try:
            q=c.cursor(dictionary=True); q.execute("SELECT id,nome,categoria,descricao,preco,ativo FROM servicos WHERE usuario_id=%s ORDER BY nome",(uid,)); return q.fetchall()
        finally: c.close()
    def buscar(self,uid,sid):
        c=get_connection()
        try:
            q=c.cursor(dictionary=True); q.execute("SELECT id,nome,categoria,descricao,preco,ativo FROM servicos WHERE id=%s AND usuario_id=%s",(sid,uid)); return q.fetchone()
        finally: c.close()
    def criar(self,uid,d):
        c=get_connection()
        try:
            q=c.cursor(); q.execute("INSERT INTO servicos(usuario_id,nome,categoria,descricao,preco,ativo) VALUES(%s,%s,%s,%s,%s,%s)",(uid,d['nome'],d.get('categoria'),d.get('descricao'),d['preco'],d.get('ativo',True))); c.commit(); return q.lastrowid
        except Exception: c.rollback(); raise
        finally: c.close()
    def atualizar(self,uid,sid,d):
        c=get_connection()
        try:
            q=c.cursor(); q.execute("UPDATE servicos SET nome=%s,categoria=%s,descricao=%s,preco=%s,ativo=%s WHERE id=%s AND usuario_id=%s",(d['nome'],d.get('categoria'),d.get('descricao'),d['preco'],d.get('ativo',True),sid,uid)); c.commit(); return q.rowcount>0
        except Exception: c.rollback(); raise
        finally: c.close()
    def excluir(self,uid,sid):
        c=get_connection()
        try:
            q=c.cursor(); q.execute("DELETE FROM servicos WHERE id=%s AND usuario_id=%s",(sid,uid)); c.commit(); return q.rowcount>0
        except Exception: c.rollback(); raise
        finally: c.close()
