CREATE DATABASE IF NOT EXISTS banco_projeto
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE banco_projeto;

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    tipo VARCHAR(20) NOT NULL DEFAULT 'empreendedor',
    data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20),
    endereco TEXT,
    data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE status_orcamento (
    id_status INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE servicos (
    id_servico INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    nome_servico VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco_padrao DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE orcamentos (
    id_orcamento INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_status INT NOT NULL,
    data_emissao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    valor_total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    observacoes TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (id_status) REFERENCES status_orcamento(id_status)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE itens_orcamento (
    id_item INT AUTO_INCREMENT PRIMARY KEY,
    id_orcamento INT NOT NULL,
    id_servico INT NOT NULL,
    quantidade INT NOT NULL,
    valor_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    CHECK (quantidade > 0),
    CHECK (valor_unitario >= 0),
    CHECK (subtotal >= 0),
    FOREIGN KEY (id_orcamento) REFERENCES orcamentos(id_orcamento)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_servico) REFERENCES servicos(id_servico)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE INDEX idx_clientes_usuario ON clientes(id_usuario);
CREATE INDEX idx_servicos_usuario ON servicos(id_usuario);
CREATE INDEX idx_orcamentos_cliente ON orcamentos(id_cliente);
CREATE INDEX idx_orcamentos_status ON orcamentos(id_status);
CREATE INDEX idx_itens_orcamento ON itens_orcamento(id_orcamento);
CREATE INDEX idx_itens_servico ON itens_orcamento(id_servico);
