from database.connection import get_connection
class UsuarioDAO:
    def buscar_por_email(self, email):
        conn=get_connection()
        try:
            cur=conn.cursor(dictionary=True)
            cur.execute("SELECT id,nome,email,senha_hash FROM usuarios WHERE email=%s",(email.lower(),))
            return cur.fetchone()
        finally: conn.close()
    def buscar_por_id(self, uid):
        conn=get_connection()
        try:
            cur=conn.cursor(dictionary=True)
            cur.execute("SELECT id,nome,email FROM usuarios WHERE id=%s AND ativo=TRUE",(uid,))
            return cur.fetchone()
        finally: conn.close()
    def criar(self,nome,email,senha_hash):
        conn=get_connection()
        try:
            cur=conn.cursor()
            cur.execute("INSERT INTO usuarios(nome,email,senha_hash) VALUES(%s,%s,%s)",(nome,email.lower(),senha_hash))
            uid=cur.lastrowid
            cur.execute("INSERT INTO empresas(usuario_id,nome) VALUES(%s,%s)",(uid,nome))
            conn.commit()
            return uid
        except Exception:
            conn.rollback(); raise
        finally: conn.close()
