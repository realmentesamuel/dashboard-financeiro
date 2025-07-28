import sqlite3
import sys

match sys.argv[1:]:

    case ['inserir',nome, preco, img]:
        with sqlite3.Connection("banco.db") as conn:
            sql_inserir_gastos = '''
            INSERT INTO produtos (nome, preco, img) VALUES (?,?,?);
            ''' 
            conn.execute(sql_inserir_gastos, (nome, preco, img))
            print('inserido.')