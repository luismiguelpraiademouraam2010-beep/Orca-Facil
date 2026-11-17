# OrçaFácil — Backend Flask + MySQL

## Estrutura
`app.py` inicia a API; `models/` contém classes POO; `dao/` contém consultas e operações no MySQL; `routes/` contém os endpoints; `database/schema.sql` cria o banco.

## 1. Criar o banco
Abra `database/schema.sql` no MySQL Workbench ou phpMyAdmin e execute. O banco criado se chama `orcafacil`.

## 2. Preparar o Python
No terminal, dentro desta pasta:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
Copie `.env.example` para `.env` e informe a senha do seu MySQL. Não envie `.env` ao GitHub.

## 3. Iniciar
```bash
python app.py
```
Teste `http://127.0.0.1:5000/` e `http://127.0.0.1:5000/api/status`.

## Rotas
As rotas abaixo, exceto registro, login e status, exigem `Authorization: Bearer TOKEN`.

| Método | Rota | Função |
|---|---|---|
| POST | `/api/auth/register` | Cadastro de usuário |
| POST | `/api/auth/login` | Login |
| GET | `/api/auth/me` | Consultar usuário autenticado |
| GET/POST | `/api/clientes` | Listar / cadastrar clientes |
| GET/PUT/DELETE | `/api/clientes/<id>` | Consultar / editar / excluir cliente |
| GET/POST | `/api/servicos` | Listar / cadastrar serviços |
| GET/PUT/DELETE | `/api/servicos/<id>` | Consultar / editar / excluir serviço |
| GET/POST | `/api/orcamentos` | Listar / criar orçamento |
| GET/DELETE | `/api/orcamentos/<id>` | Consultar / excluir orçamento |
| PATCH | `/api/orcamentos/<id>/status` | Alterar status |
| GET | `/api/orcamentos/relatorio/resumo` | Indicadores para dashboard |
| GET/PUT | `/api/empresa` | Consultar / atualizar empresa |

## Exemplos de JSON

Registro:
```json
{"nome":"Luís","email":"luis@email.com","senha":"senha12345"}
```
Cliente:
```json
{"nome":"Mariana Costa","email":"mariana@email.com","telefone":"(19) 98888-1111","empresa":"Studio MC"}
```
Serviço:
```json
{"nome":"Criação de site","categoria":"Desenvolvimento","descricao":"Site responsivo","preco":1800}
```
Orçamento:
```json
{"cliente_id":1,"descricao":"Projeto de site","validade":"2026-12-15","desconto":100,"itens":[{"servico_id":1,"quantidade":1}]}
```

## Integração com o frontend
A interface atual ainda usa `localStorage`. Na etapa de integração, substitua as funções de leitura e gravação por `fetch` e envie o token JWT em `Authorization`.

Exemplo GET:
```javascript
const resposta = await fetch('http://127.0.0.1:5000/api/clientes', {
  headers: { Authorization: `Bearer ${token}` }
});
const clientes = await resposta.json();
```
Exemplo POST:
```javascript
const resposta = await fetch('http://127.0.0.1:5000/api/clientes', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`
  },
  body: JSON.stringify({nome:'Mariana Costa',email:'mariana@email.com'})
});
const resultado = await resposta.json();
```

Cada usuário acessa apenas seus próprios registros. Senhas são armazenadas com hash e as consultas SQL usam parâmetros. Teste no MySQL local antes da apresentação.
