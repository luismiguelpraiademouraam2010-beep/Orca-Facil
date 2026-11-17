CREATE DATABASE IF NOT EXISTS orcafacil CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE orcafacil;

CREATE TABLE IF NOT EXISTS usuarios (
 id INT AUTO_INCREMENT PRIMARY KEY,
 nome VARCHAR(120) NOT NULL,
 email VARCHAR(180) NOT NULL UNIQUE,
 senha_hash VARCHAR(255) NOT NULL,
 ativo BOOLEAN NOT NULL DEFAULT TRUE,
 criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS empresas (
 id INT AUTO_INCREMENT PRIMARY KEY,
 usuario_id INT NOT NULL UNIQUE,
 nome VARCHAR(160) NOT NULL,
 cnpj VARCHAR(20), email VARCHAR(180), telefone VARCHAR(30),
 endereco VARCHAR(255), descricao TEXT,
 criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 CONSTRAINT fk_empresas_usuario FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS clientes (
 id INT AUTO_INCREMENT PRIMARY KEY,
 usuario_id INT NOT NULL,
 nome VARCHAR(150) NOT NULL,
 email VARCHAR(180) NOT NULL,
 telefone VARCHAR(30), empresa VARCHAR(160),
 criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 CONSTRAINT fk_clientes_usuario FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
 INDEX idx_clientes_usuario_nome(usuario_id,nome),
 INDEX idx_clientes_usuario_email(usuario_id,email)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS servicos (
 id INT AUTO_INCREMENT PRIMARY KEY,
 usuario_id INT NOT NULL,
 nome VARCHAR(160) NOT NULL,
 categoria VARCHAR(100), descricao TEXT,
 preco DECIMAL(12,2) NOT NULL DEFAULT 0.00,
 ativo BOOLEAN NOT NULL DEFAULT TRUE,
 criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 CONSTRAINT fk_servicos_usuario FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
 INDEX idx_servicos_usuario_nome(usuario_id,nome)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS orcamentos (
 id INT AUTO_INCREMENT PRIMARY KEY,
 usuario_id INT NOT NULL,
 cliente_id INT NOT NULL,
 descricao VARCHAR(255) NOT NULL,
 data_orcamento DATE NOT NULL,
 validade DATE NULL,
 desconto DECIMAL(12,2) NOT NULL DEFAULT 0.00,
 total DECIMAL(12,2) NOT NULL DEFAULT 0.00,
 status ENUM('Pendente','Aprovado','Rejeitado') NOT NULL DEFAULT 'Pendente',
 criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 CONSTRAINT fk_orcamentos_usuario FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
 CONSTRAINT fk_orcamentos_cliente FOREIGN KEY(cliente_id) REFERENCES clientes(id) ON DELETE RESTRICT,
 INDEX idx_orcamentos_usuario_data(usuario_id,data_orcamento),
 INDEX idx_orcamentos_usuario_status(usuario_id,status)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS itens_orcamento (
 id INT AUTO_INCREMENT PRIMARY KEY,
 orcamento_id INT NOT NULL,
 servico_id INT NOT NULL,
 quantidade INT NOT NULL DEFAULT 1,
 preco_unitario DECIMAL(12,2) NOT NULL,
 subtotal DECIMAL(12,2) NOT NULL,
 CONSTRAINT fk_itens_orcamento FOREIGN KEY(orcamento_id) REFERENCES orcamentos(id) ON DELETE CASCADE,
 CONSTRAINT fk_itens_servico FOREIGN KEY(servico_id) REFERENCES servicos(id) ON DELETE RESTRICT,
 CONSTRAINT chk_itens_quantidade CHECK(quantidade > 0),
 INDEX idx_itens_orcamento(orcamento_id)
) ENGINE=InnoDB;