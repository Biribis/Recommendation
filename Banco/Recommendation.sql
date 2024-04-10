CREATE DATABASE Recommendation;
USE Recommendation;

CREATE TABLE tb_usuario(          
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(50) NOT NULL,
    email_usuario VARCHAR(50) NOT NULL,
    senha_usuario VARCHAR(50) NOT NULL,
    idade_usuario INT NOT NULL
    );
    
CREATE TABLE tb_genero(
	id_genero INT AUTO_INCREMENT PRIMARY KEY,
	id_genero_usuario INT NOT NULL,
    nome_genero VARCHAR(50),
    FOREIGN KEY (id_genero_usuario) REFERENCES tb_usuario(id_usuario)
);

CREATE TABLE tb_jogos(          
    id_jogos INT AUTO_INCREMENT PRIMARY KEY,
    nome_jogos VARCHAR(50) NOT NULL,
    genero_jogos VARCHAR(50) NOT NULL,
    plataforma_jogos ENUM('PC', 'Mobile', 'Console', 'Multi-plataforma') NOT NULL,
    faixaetaria_jogos INT NOT NULL
    );
    
CREATE TABLE tb_usuario_jogos(
    id_usuario_jogos INT AUTO_INCREMENT PRIMARY KEY,
    tempototal_usuario_jogos INT NOT NULL,
    usuario_id_fk INT NOT NULL,
    jogos_id_fk INT NOT NULL,
    FOREIGN KEY (usuario_id_fk) REFERENCES tb_usuario(id_usuario),
    FOREIGN KEY (jogos_id_fk) REFERENCES tb_jogos(id_jogos)
    );