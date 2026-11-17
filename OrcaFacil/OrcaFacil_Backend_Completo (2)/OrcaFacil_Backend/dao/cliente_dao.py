from database.connection import get_connection
class ClienteDAO:
    def listar(self,uid):
        c=get_connection()
        try:
            q=c.cursor(dictionary=True); q.execute("SELECT id,nome,email,telefone,empresa FROM clientes WHERE usuario_id=%s ORDER BY nome",(uid,)); return q.fetchall()
        finally: c.close()
    def buscar(self,uid,cid):
        c=get_connection()
        try:
            q=c.cursor(dictionary=True); q.execute("SELECT id,nome,email,telefone,empresa FROM clientes WHERE id=%s AND usuario_id=%s",(cid,uid)); return q.fetchone()
        finally: c.close()
    def criar(self,uid,d):
        c=get_connection()
        try:
            q=c.cursor(); q.execute("INSERT INTO clientes(usuario_id,nome,email,telefone,empresa) VALUES(%s,%s,%s,%s,%s)",(uid,d['nome'],d['email'].lower(),d.get('telefone'),d.get('empresa'))); c.commit(); return q.lastrowid
        except Exception: c.rollback(); raise
        finally: c.close()
    def atualizar(self,uid,cid,d):
        c=get_connection()
        try:
            q=c.cursor(); q.execute("UPDATE clientes SET nome=%s,email=%s,telefone=%s,empresa=%s WHERE id=%s AND usuario_id=%s",(d['nome'],d['email'].lower(),d.get('telefone'),d.get('empresa'),cid,uid)); c.commit(); return q.rowcount>0
        except Exception: c.rollback(); raise
        finally: c.close()
    def excluir(self,uid,cid):
        c=get_connection()
        try:
            q=c.cursor(); q.execute("DELETE FROM clientes WHERE id=%s AND usuario_id=%s",(cid,uid)); c.commit(); return q.rowcount>0
        except Exception: c.rollback(); raise
        finally: c.close()
