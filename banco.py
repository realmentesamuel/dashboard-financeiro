import sqlite3

conn = sqlite3.Connection('banco.db')

sql_criar_tabela_usuarios = '''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    login TEXT NOT NULL,
    senha TEXT NOT NULL,
    email TEXT
);
'''

sql_produtos = '''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY,
	img TEXT NOT NULL,
	preco TEXT NOT NULL,
	nome TEXT NOT NULL
);
'''
sql_despesas = '''
CREATE TABLE IF NOT EXISTS despesas (
    id INTEGER PRIMARY KEY,
    valor REAL NOT NULL
);
'''

sql_salario = '''
CREATE TABLE IF NOT EXISTS salario (
    id INTEGER PRIMARY KEY DEFAULT 1,
    slr REAL NOT NULL
);
'''

conn.execute(sql_salario)
conn.execute(sql_despesas)
conn.execute(sql_criar_tabela_usuarios)
conn.execute(sql_produtos)
conn.commit()

sql_insert_gastos = '''
INSERT INTO produtos (img, preco, nome) VALUES (?, ?, ?);
'''
lista_de_gastos = [
    ('1.jpg','700,00','Aluguel'),

    ('2.jpg','150,00','Água'),
    
    ('3.jpg','250,00','Luz')
]

conn.executemany(sql_insert_gastos, lista_de_gastos)

sql_insert_usuarios = '''
INSERT INTO usuarios (login, senha, email) VALUES (?,?,?);
'''
lista_de_usuarios = [
    ('admin','0000', 'email@senacrs.edu.br'),
    ('usuario', 'senha', 'teste@email.com')
]

conn.executemany(sql_insert_usuarios, lista_de_usuarios)

conn.commit()
conn.close()