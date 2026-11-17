class Servico:
    def __init__(self, nome, preco, categoria=None, descricao=None, id=None, ativo=True):
        self.id, self.nome, self.preco = id, nome, float(preco)
        self.categoria, self.descricao, self.ativo = categoria, descricao, bool(ativo)
    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "preco": self.preco,
                "categoria": self.categoria, "descricao": self.descricao, "ativo": self.ativo}
