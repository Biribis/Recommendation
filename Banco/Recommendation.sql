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
    favorito bool NOT NULL,
    FOREIGN KEY (usuario_id_fk) REFERENCES tb_usuario(id_usuario),
    FOREIGN KEY (jogos_id_fk) REFERENCES tb_jogos(id_jogos)
    );
    
    INSERT INTO tb_jogos(nome_jogos, genero_jogos, plataforma_jogos, faixaetaria_jogos) VALUES
	('Call of Duty: Warzone', 'FPS', 'Multi-plataforma', 18),
	('Counter-Strike: Global Offensive', 'FPS', 'PC', 18),
	('Overwatch', 'FPS', 'Multi-plataforma', 13),
	('Rainbow Six Siege', 'FPS', 'Multi-plataforma', 18),
	('DOOM Eternal', 'FPS', 'Multi-plataforma', 18),
	('Battlefield V', 'FPS', 'Multi-plataforma', 18),
	('Halo Infinite', 'FPS', 'Multi-plataforma', 18),
  ('FIFA 22', 'Sport', 'Multi-plataforma', 0),
  ('NBA 2K22', 'Sport', 'Multi-plataforma', 0),
  ('Madden NFL 22', 'Sport', 'Multi-plataforma', 0),
  ('Pro Evolution Soccer 2023', 'Sport', 'Multi-plataforma', 0),
  ('MLB The Show 22', 'Sport', 'Console', 0),
  ('Rocket League', 'Sport', 'Multi-plataforma', 0),
  ('Tony Hawks Pro Skater 1 + 2', 'Sport', 'Multi-plataforma', 13),
  ('League of Legends', 'MOBA', 'PC', 13),
  ('Dota 2', 'MOBA', 'PC', 18),
  ('Smite', 'MOBA', 'Multi-plataforma', 13),
  ('Heroes of the Storm', 'MOBA', 'PC', 13),
  ('Arena of Valor', 'MOBA', 'Multi-plataforma', 10),
  ('Vainglory', 'MOBA', 'Mobile', 10),
  ('Mobile Legends: Bang Bang', 'MOBA', 'Mobile', 13),
  ('The Witcher 3: Wild Hunt', 'RPG', 'Multi-plataforma', 18),
  ('Final Fantasy XIV', 'RPG', 'Multi-plataforma', 13),
  ('The Elder Scrolls V: Skyrim', 'RPG', 'Multi-plataforma', 18),
  ('Divinity: Original Sin 2', 'RPG', 'Multi-plataforma', 18),
  ('Dragon Age: Inquisition', 'RPG', 'Multi-plataforma', 18),
  ('Persona 5', 'RPG', 'Console', 13),
  ('Octopath Traveler', 'RPG', 'Console', 13);
