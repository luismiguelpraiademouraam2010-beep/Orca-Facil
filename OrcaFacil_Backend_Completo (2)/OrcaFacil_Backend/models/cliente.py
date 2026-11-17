class Cliente:
    def __init__(self, nome, email, telefone=None, empresa=None, id=None):
        self.id, self.nome, self.email = id, nome, email
        self.telefone, self.empresa = telefone, empresa
    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "email": self.email,
                "telefone": self.telefone, "empresa": self.empresa}
