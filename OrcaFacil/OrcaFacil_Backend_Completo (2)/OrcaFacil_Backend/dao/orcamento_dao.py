from database.connection import get_connection
class OrcamentoDAO:
    def listar(self,uid):
        c=get_connection()
        try:
            q=c.cursor(dictionary=True)
            q.execute("""SELECT o.id,o.cliente_id,c.nome AS cliente,o.descricao,o.data_orcamento AS data,
                         o.validade,o.desconto,o.total,o.status FROM orcamentos o
                         JOIN clientes c ON c.id=o.cliente_id WHERE o.usuario_id=%s ORDER BY o.criado_em DESC""",(uid,))
            return q.fetchall()
        finally: c.close()
    def buscar(self,uid,oid):
        c=get_connection()
        try:
            q=c.cursor(dictionary=True)
            q.execute("""SELECT o.id,o.cliente_id,c.nome AS cliente,o.descricao,o.data_orcamento AS data,
                         o.validade,o.desconto,o.total,o.status FROM orcamentos o JOIN clientes c ON c.id=o.cliente_id
                         WHERE o.id=%s AND o.usuario_id=%s""",(oid,uid))
            item=q.fetchone()
            if item:
                q.execute("""SELECT i.servico_id,s.nome,i.quantidade,i.preco_unitario,i.subtotal
                             FROM itens_orcamento i JOIN servicos s ON s.id=i.servico_id WHERE i.orcamento_id=%s""",(oid,))
                item['itens']=q.fetchall()
            return item
        finally: c.close()
    def criar(self,uid,d,itens):
        c=get_connection()
        try:
            q=c.cursor(dictionary=True)
            q.execute("SELECT id FROM clientes WHERE id=%s AND usuario_id=%s",(d['cliente_id'],uid))
            if not q.fetchone(): raise ValueError("Cliente não encontrado nesta conta.")
            ids=[int(x['servico_id']) for x in itens]
            if not ids: raise ValueError("Adicione pelo menos um item.")
            marks=','.join(['%s']*len(ids))
            q.execute(f"SELECT id,preco FROM servicos WHERE usuario_id=%s AND ativo=TRUE AND id IN ({marks})",tuple([uid]+ids))
            prices={r['id']:float(r['preco']) for r in q.fetchall()}
            if len(prices)!=len(set(ids)): raise ValueError("Serviço inexistente ou inativo.")
            lines=[]; bruto=0
            for item in itens:
                sid=int(item['servico_id']); qty=int(item.get('quantidade',1))
                if qty<1: raise ValueError("Quantidade deve ser maior que zero.")
                price=prices[sid]; subtotal=price*qty; bruto+=subtotal; lines.append((sid,qty,price,subtotal))
            desconto=float(d.get('desconto',0))
            if desconto<0 or desconto>bruto: raise ValueError("Desconto inválido.")
            cur=c.cursor()
            cur.execute("""INSERT INTO orcamentos(usuario_id,cliente_id,descricao,data_orcamento,validade,desconto,total,status)
                           VALUES(%s,%s,%s,%s,%s,%s,%s,'Pendente')""",
                        (uid,d['cliente_id'],d.get('descricao') or 'Orçamento',d['data_orcamento'],d.get('validade'),desconto,bruto-desconto))
            oid=cur.lastrowid
            cur.executemany("""INSERT INTO itens_orcamento(orcamento_id,servico_id,quantidade,preco_unitario,subtotal)
                               VALUES(%s,%s,%s,%s,%s)""",[(oid,*line) for line in lines])
            c.commit(); return oid
        except Exception: c.rollback(); raise
        finally: c.close()
    def atualizar_status(self,uid,oid,status):
        c=get_connection()
        try:
            q=c.cursor(); q.execute("UPDATE orcamentos SET status=%s WHERE id=%s AND usuario_id=%s",(status,oid,uid)); c.commit(); return q.rowcount>0
        except Exception: c.rollback(); raise
        finally: c.close()
    def excluir(self,uid,oid):
        c=get_connection()
        try:
            q=c.cursor(); q.execute("DELETE FROM orcamentos WHERE id=%s AND usuario_id=%s",(oid,uid)); c.commit(); return q.rowcount>0
        except Exception: c.rollback(); raise
        finally: c.close()
    def resumo(self,uid):
        c=get_connection()
        try:
            q=c.cursor(dictionary=True)
            q.execute("""SELECT COUNT(*) quantidade,COALESCE(SUM(total),0) valor_total,
                         COALESCE(SUM(CASE WHEN status='Aprovado' THEN total ELSE 0 END),0) valor_aprovado,
                         COALESCE(SUM(status='Aprovado'),0) aprovados,
                         COALESCE(SUM(status='Pendente'),0) pendentes,
                         COALESCE(SUM(status='Rejeitado'),0) rejeitados
                         FROM orcamentos WHERE usuario_id=%s""",(uid,))
            return q.fetchone()
        finally: c.close()
