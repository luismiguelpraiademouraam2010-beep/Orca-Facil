# OrçaFácil — Backend local

## Requisitos
- Python 3.10 ou superior
- XAMPP com MySQL/MariaDB iniciado
- Navegador atualizado

## 1. Criar o banco
1. Abra o XAMPP e inicie **MySQL**.
2. Entre em http://localhost/phpmyadmin
3. Clique em **Importar** e selecione `backend/schema.sql`.
4. Execute a importação. O banco `orcafacil` e as tabelas serão criados.

## 2. Instalar dependências
Abra o terminal na pasta do projeto e execute:

```powershell
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r backend/requirements.txt
```

## 3. Iniciar o sistema
Na raiz do projeto:

```powershell
py backend/app.py
```

Abra **http://127.0.0.1:5000**. Use este endereço para testar o backend; o endereço GitHub Pages é apenas hospedagem estática e não executa Python.

## Observações
- O cadastro e login da API armazenam hash da senha, não a senha em texto puro.
- A sessão é mantida por cookie HTTP-only.
- Configure uma chave secreta própria e uma senha para o MySQL antes de colocar o sistema em produção.
- Não publique credenciais reais no GitHub.
