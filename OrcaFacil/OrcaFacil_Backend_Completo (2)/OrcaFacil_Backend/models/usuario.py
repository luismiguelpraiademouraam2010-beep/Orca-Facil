class Usuario:
    def __init__(self, nome, email, senha_hash, id=None):
        self.id, self.nome, self.email, self.senha_hash = id, nome, email, senha_hash
    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "email": self.email}
