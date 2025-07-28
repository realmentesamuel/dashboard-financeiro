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

@app.get("/editar/<id_gasto>")
def editar_produto(id_gasto):
    with sqlite3.Connection('banco.db') as conn:
        sql_dados_gastos = f'''
            SELECT id, nome, preco, img
            FROM produtos 
            WHERE id = {id_gasto}
            '''
        registro_gastos = conn.execute(sql_dados_gastos)
        id, nome, preco, img = next(registro_gastos)
        dados_gasto = {
            "id": id,
            "nome": nome,
            "preco": preco,
            "img": img,
        }
        
        return flask.render_template("editar_gasto.html",
                                     gasto = dados_gasto)

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
        preco="{preco}",
    WHERE produtos.id = {id}    
'''
    with sqlite3.Connection('banco.db') as conn:
        conn.execute(sql_atualizar_produto)
        conn.commit()

    return flask.redirect("/")

app.run(host='0.0.0.0', debug=True)