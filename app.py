import flask
import sqlite3
from secrets import token_hex

app = flask.Flask(__name__)

app.secret_key = token_hex()

@app.get("/")
def get_home():
    return flask.render_template("home.html")

@app.get("/login")
def get_login():
    return flask.render_template("login.html")

@app.post("/login")
def post_login():
    login = flask.request.form['login']
    senha = flask.request.form['senha']
    
    sql_validar_login = f'''
    SELECT login, senha, email
    FROM usuarios
    WHERE 
        login="{login}" AND senha="{senha}";
'''
    print(sql_validar_login)
    with sqlite3.Connection('banco.db') as conn:
        dados_usuario = conn.execute(sql_validar_login)

        try:
            login, _, email = next(dados_usuario)
            flask.session["login"] = login
            flask.session["email"] = email        
        except StopIteration:
            return flask.redirect("/")
        
    return flask.redirect("/")

@app.get("/logout")
def get_logout():
    flask.session.clear()
    return flask.redirect('/')

@app.get('/controle')
def get_produtos():
    sql_select_gastos = '''
    SELECT img, preco, nome, id FROM produtos ORDER BY preco DESC;
'''
    with sqlite3.Connection('banco.db') as conn:
        lista_de_gastos = conn.execute(sql_select_gastos)
    
    return flask.render_template("controle.html", produtos=lista_de_gastos)

@app.get("/cadastrar")
def get_cadastrar():
    return flask.render_template("cadastrar.html")

@app.post("/cadastrar")
def post_cadastrar():

    nome  = flask.request.form.get("nome")
    preco = flask.request.form.get("preco")
    img = flask.request.form.get("img")

    with sqlite3.Connection("banco.db") as conn:
        sql_inserir_produto = '''
        INSERT INTO produtos (nome, preco, img) VALUES (?,?,?);
        ''' 
        conn.execute(sql_inserir_produto, (nome, preco, img))

    return flask.redirect("/controle")

@app.get("/editar/<id_produto>")
def editar_produto(id_produto):
    with sqlite3.Connection('banco.db') as conn:
        sql_dados_produto = f'''
            SELECT id, nome, preco, img
            FROM produtos 
            WHERE id = {id_produto}
            '''
        registro_produto = conn.execute(sql_dados_produto)
        id, nome, preco, img = next(registro_produto)
        dados_produto = {
            "id": id,
            "nome": nome,
            "preco": preco,
            "img": img,
        }
        
        return flask.render_template("editar_gasto.html",
                                     produto = dados_produto)

@app.post("/atualizar")
def atualizar_produto():
    id = flask.request.form['id']
    nome = flask.request.form['nome']
    preco = flask.request.form['preco']
    img = flask.request.form['img']
    
    sql_atualizar_produto = f'''
    UPDATE produtos 
    SET img="{img}",
        nome="{nome}",
        preco="{preco}"
    WHERE produtos.id = {id}    
'''
    with sqlite3.Connection('banco.db') as conn:
        conn.execute(sql_atualizar_produto)
        conn.commit()

    return flask.redirect("/controle")
        
@app.get("/excluir/<id_produto>")
def excluir_produto(id_produto):
    sql_excluir_produto = f'''
    DELETE FROM produtos WHERE id = {id_produto}
    '''
    with sqlite3.Connection('banco.db') as conn:
        conn.execute(sql_excluir_produto)
        conn.commit
    
    return flask.redirect("/")

@app.get("/salario")
def get_salario():
    return flask.render_template("salario.html")

@app.post("/salario")
def post_salario():
    
    try:
        valor  = float(flask.request.form.get("salario"))
        with sqlite3.Connection("banco.db") as conn:
            sql_salario = "REPLACE INTO salario (id, slr) VALUES (1, ?)";
            conn.execute(sql_salario, (valor,))
    except ValueError:
        return flask.redirect('/')
    
    try:
        with sqlite3.Connection("banco.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT preco FROM produtos")
            precos = cursor.fetchall()
            total = 0.0
            for preco in precos:
                total += float(str(preco[0]).replace(',','.'))
            calculo = valor - total
            
            print(calculo)
            
    except ValueError:
        return None
    
    return flask.redirect("/controle")
    

app.run(host='0.0.0.0', debug=True)