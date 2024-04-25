from flask import Flask, request, jsonify, render_template
from flask_login import current_user, LoginManager, login_user, logout_user, login_required, UserMixin
from DAO import DAO
from datetime import date
def calculate_age(born):
    ano = born[0] + born[1] + born[2] + born[3]
    mes = born[5] + born[6]
    dia = born[8] + born[9]
    today = date.today()
    return today.year - int(ano) - ((today.month, today.day) < (int(mes), int(dia)))

app = Flask(__name__)
app.secret_key = 'ahampohissoaimsm'

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
        return jsonify({"status": 401,
                        "reason": "Erro de Login"})

# Tela de logout (?)
# @app.route('/logout', methods=['GET'])
# def logout():
#     logout_user()
#     return render_template('login.html')

@app.route('/perfil')
@login_required
def perfil():
    dao = DAO('tb_genero')
    id = current_user.id_usuario
    nome = current_user.nome_usuario
    lista = dao.readBy('id_genero_usuario', '==', id)
    if len(lista) == 1:
        a = 0
        genero = lista[0].nome_genero
        return render_template('perfil.html', nome=nome, genero=genero, a=a)
    else:
        a = 1
        registro = lista[0]
        registro2 = lista[1]
        genero = registro.nome_genero
        genero2 = registro2.nome_genero
        return render_template('perfil.html', nome=nome, genero = genero, genero2=genero2, a=a)

@app.route('/search')
def search():
    digit = request.args.get('search', '')
    dao = DAO('tb_jogos')
    if digit == '':
        a = 1
        return render_template('index.html', a=a)
    else:
        a = 0
        lista = dao.readBy('nome_jogos', 'ilike', digit)
        if len(lista) == 0:
            return render_template('index.html', digit=digit, a=a)
        else:
            return render_template('jogo-info.html', lista=lista, a=a)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
