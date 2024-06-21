from flask import Flask, request, jsonify, render_template, redirect
from flask_login import current_user, LoginManager, login_user, logout_user, login_required, UserMixin
from DAO import DAO
from datetime import date
from random import randint
from flask_mysqldb import MySQL
import csv
from csv_handling import avaliar, recomendar
def calculate_age(born):
    ano = born[0] + born[1] + born[2] + born[3]
    mes = born[5] + born[6]
    dia = born[8] + born[9]
    today = date.today()
    return today.year - int(ano) - ((today.month, today.day) < (int(mes), int(dia)))

app = Flask(__name__)
app.secret_key = 'ahampohissoaimsm'

mysql = MySQL(app)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "quemleumecomeu"
app.config["MYSQL_DB"] = "Recommendation"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    id_usuario = 0
    nome_usuario = ''
    email_usuario = ''
    senha_usuario = ''
    idade_usuario = ''

    def to_json(self):
        return {
            "id_usuario": self.id_usuario,
            "nome_usuario": self.nome_usuario,
            "email_usuario": self.email_usuario,
            "senha_usuario": self.senha_usuario,
            "idade_usuario": self.idade_usuario}

    def get_id(self):
        return str(self.id_usuario)

# Listagem dos usuários válidos
@login_manager.user_loader
def load_user(user_id):
    dao = DAO('tb_usuario')
    lista = dao.readBy('id_usuario', '==', user_id)
    if len(lista) == 1:
        usr = User()
        usr.id_usuario = str(lista[0].id_usuario)
        usr.username = lista[0].nome_usuario
        usr.email_usuario = lista[0].email_usuario
        usr.idade_usuario = lista[0].idade_usuario
        return usr
    else:
        return None

# Tela inicial
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/2')
def index2():
    daoUsr = DAO('tb_usuario')
    id = daoUsr.selectid('id_usuario')
    daoUsr.deletelastid('id_usuario', id)

    return render_template('index.html')

@app.route('/render_cadastro')
def render_cadastro():
    return render_template('cadastro.html')

@app.route('/cadastro', methods=['GET'])
def cadastro():
    daoUsr = DAO('tb_usuario')
    objUsr = daoUsr.tb_usuario()
    objUsr.nome_usuario = request.args.get('name')
    nome = objUsr.nome_usuario
    objUsr.email_usuario = request.args.get('email')
    objUsr.senha_usuario = request.args.get('password')
    data = request.args.get('idade')
    objUsr.idade_usuario = calculate_age(data)

    lista = daoUsr.readBy('email_usuario', '==', objUsr.email_usuario)
    if len(lista) == 1:
        return jsonify({"status": 401,
                        "reason": "User already exists"})
    else:
        daoUsr.create(objUsr)
        usuario_criado = daoUsr.readBy('nome_usuario', '==', nome)
        daoJog = DAO('tb_jogos')
        lista_jogos = daoJog.readAll()
        arquivo_csv = "banco/usuario_jogos.csv"
        with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as arquivo:
            escritor_csv = csv.writer(arquivo)
            for i in range(len(lista_jogos)):
                jogo_csv = [usuario_criado[0].id_usuario, lista_jogos[i].id_jogos, 0, 0]
                escritor_csv.writerow(jogo_csv)
        return render_template("cadastro2.html")
    
@app.route('/cadastro2', methods=['GET'])
def cadastro2():
    daoGen = DAO('tb_genero')
    daoUsr = DAO('tb_usuario')
    id = daoUsr.selectid('id_usuario')

    objGen = daoGen.tb_genero()
    objGen2 = daoGen.tb_genero()
    objGen.id_genero_usuario = id
    objGen2.id_genero_usuario = id
    objGen.nome_genero = request.args.get('genero')
    objGen2.nome_genero = request.args.get('genero2')

    if objGen.nome_genero == objGen2.nome_genero:
        daoGen.create(objGen)
    else:
        daoGen.create(objGen)
        daoGen.create(objGen2)

    return render_template("index.html")

@app.route('/render_login')
def render_login():
    return render_template('login.html')

# Login do usuário
@app.route('/login', methods=['GET'])
def login():
    usuario = request.args.get('name')
    senha = request.args.get('password')
    print(usuario, senha)
    dao = DAO('tb_usuario')
    lista = dao.readBy('nome_usuario', '==', usuario)
    if len(lista) == 1 and lista[0].senha_usuario:
        usr = User()
        usr.id_usuario = str(lista[0].id_usuario)
        usr.nome_usuario = lista[0].nome_usuario
        usr.email_usuario = lista[0].email_usuario
        usr.senha_usuario = lista[0].senha_usuario
        usr.idade_usuario = lista[0].idade_usuario
        login_user(usr, remember=True)

        if current_user.is_authenticated:
            # Autentica o usuário novamente para que o método login_remembered() funcione corretamente
            return render_template('index.html')
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/render_login')

@app.route('/perfil')
@login_required
def perfil():
    dao = DAO('tb_genero')
    lista = dao.readBy('id_genero_usuario', '==', current_user.id_usuario)
    daoUJ = DAO('tb_usuario_jogos')
    lista_jogos = daoUJ.readBy('usuario_id_fk', '==', current_user.id_usuario)
    daoJog = DAO('tb_jogos')
    lista_fav = []
    temp_jog = []
    temp_fav = []
    for i in lista_jogos:
        tab_jog = daoJog.readById(i.jogos_id_fk)
        if i.favorito == 1:
            lista_fav.append(tab_jog)
            temp_fav.append(i.tempototal_usuario_jogos)
            lista_jogos.remove(i)
        else:
            lista_jogos.append(tab_jog)
            temp_jog.append(i.tempototal_usuario_jogos)
            lista_jogos.remove(i)

    favoritos = zip(lista_fav, temp_fav)
    jogos = zip(lista_jogos, temp_jog)

    if len(lista) == 1:
        genero = lista[0].nome_genero
        return render_template('perfil.html', current_user=current_user, genero=genero, a=0, favoritos=favoritos, jogos=jogos)
    else:
        registro = lista[0]
        registro2 = lista[1]
        genero = registro.nome_genero
        genero2 = registro2.nome_genero
        return render_template('perfil.html', genero=genero, genero2=genero2, a=1, favoritos=favoritos, jogos=jogos, user=current_user)

@app.route('/add', methods=["POST"])
@login_required
def add():
    daoJog = DAO('tb_jogos')
    daoUJ = DAO('tb_usuario_jogos')

    game_id = request.form['game_id']

    linha = daoJog.readBy('id_jogos','==', game_id)

    objUJ = daoUJ.tb_usuario_jogos()
    objUJ.tempototal_usuario_jogos = randint(0, 1000)
    objUJ.usuario_id_fk = current_user.id_usuario
    objUJ.jogos_id_fk = linha[0].id_jogos
    objUJ.favorito = 0
    objUJ.avaliacao_usuario_jogos = 0
    daoUJ.create(objUJ)

    return render_template('jogo_solo.html', user=current_user, linha=linha[0], a=1)

@app.route('/favourite', methods=["POST"])
@login_required
def favourite():
    daoUJ = DAO('tb_usuario_jogos')
    game_id = request.form['id_game']
    daoUJ.altFavourite(game_id, current_user.id_usuario, 1)

    return render_template('perfil.html', user=current_user, a=2)

@app.route('/search', methods=["POST","GET"])
def search():
    if current_user.is_authenticated:
        if current_user.idade_usuario >= 18:
            cursor = mysql.connection.cursor()
            if request.method == 'POST':
                searchbox = request.form['query']
                print(searchbox)
                if searchbox == " ":
                    query = "SELECT * from tb_jogos;"
                    cursor.execute(query)
                    jogos = cursor.fetchall()
                elif searchbox != " ":
                    query = f"SELECT * FROM tb_jogos WHERE nome_jogos LIKE '%{searchbox}%';"
                    cursor.execute(query)
                    jogos = cursor.fetchall()
                daoUJ = DAO('tb_usuario_jogos')
                ids = daoUJ.readBy('usuario_id_fk', '==', current_user.id_usuario)
                for i in range(len(ids)):
                    ids.append(ids[i].jogos_id_fk)
                    ids.remove(ids[i])
                jogos = [jogo for jogo in jogos if jogo['id_jogos'] not in ids]
            return jsonify({'htmlresponse': render_template('jogo-info.html', jogos=jogos)})
        else:
            cursor = mysql.connection.cursor()
            if request.method == 'POST':
                searchbox = request.form['query']
                print(searchbox)
                if searchbox == " ":
                    query = "SELECT * from tb_jogos WHERE faixaetaria_jogos < 18;"
                    cursor.execute(query)
                    jogos = cursor.fetchall()
                elif searchbox != " ":
                    query = f"SELECT * FROM tb_jogos WHERE faixaetaria_jogos < 18 AND nome_jogos LIKE '%{searchbox}%';"
                    cursor.execute(query)
                    jogos = cursor.fetchall()
                daoUJ = DAO('tb_usuario_jogos')
                ids = daoUJ.readBy('usuario_id_fk', '==', current_user.id_usuario)
                for i in range(len(ids)):
                    ids.append(ids[i].jogos_id_fk)
                    ids.remove(ids[i])
                jogos = [jogo for jogo in jogos if jogo['id_jogos'] not in ids]
            return jsonify({'htmlresponse': render_template('jogo-info.html', jogos=jogos)})
    else:
        cursor = mysql.connection.cursor()
        if request.method == 'POST':
            searchbox = request.form['query']
            print(searchbox)
            if searchbox == " ":
                query = "SELECT * from tb_jogos"
                cursor.execute(query)
                jogos = cursor.fetchall()
            elif searchbox != " ":
                query = f"SELECT * FROM tb_jogos WHERE nome_jogos LIKE '%{searchbox}%';"
                cursor.execute(query)
                jogos = cursor.fetchall()

        return jsonify({'htmlresponse': render_template('jogo-info.html', jogos=jogos)})

@app.route('/game', methods=['POST'])
@login_required
def game():
    game_id = request.form['id_jogo']
    print(game_id)
    daoJog = DAO('tb_jogos')
    linha = daoJog.readBy('id_jogos','==', game_id)
    print(linha[0].id_jogos)
    daoUJ = DAO('tb_usuario_jogos')
    lista = daoUJ.selectUsuJog(linha[0].id_jogos, current_user.id_usuario)
    if lista:
        return render_template('jogo_solo.html', linha=linha[0], user=current_user, a=1)
    else:
        return render_template('jogo_solo.html', linha=linha[0], user=current_user, a=0)

@app.route('/avalia', methods=['POST'])
@login_required
def avalia():
    avaliacao = request.form['avalia']
    idJ = request.form['idJ']
    print(f'nota: {avaliacao}\nidJ: {idJ}')
    dao = DAO('tb_usuario_jogos')
    daoJog = DAO('tb_jogos')
    dao.altAvalia(current_user.id_usuario, idJ, int(avaliacao))
    linha = daoJog.readBy('id_jogos', '==', idJ)
    avaliar(current_user.id_usuario, idJ, avaliacao)
    return render_template('jogo_solo.html', linha=linha[0], user=current_user, a=1)

@app.route('/recomenda')
@login_required
def recomenda():
    return 0

if __name__ == "__main__":
    app.run(port=8080, debug=True)
