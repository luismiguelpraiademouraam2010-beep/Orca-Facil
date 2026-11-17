class Orcamento:
    STATUS_VALIDOS = ("Pendente", "Aprovado", "Rejeitado")
    def __init__(self, cliente_id, descricao, data_orcamento, validade=None,
                 desconto=0, status="Pendente", id=None, total=0):
        self.id, self.cliente_id = id, int(cliente_id)
        self.descricao, self.data_orcamento, self.validade = descricao, data_orcamento, validade
        self.desconto, self.status, self.total = float(desconto), status, float(total)
    def to_dict(self):
        return {"id": self.id, "cliente_id": self.cliente_id, "descricao": self.descricao,
                "data": str(self.data_orcamento), "validade": str(self.validade) if self.validade else None,
                "desconto": self.desconto, "status": self.status, "total": self.total}
