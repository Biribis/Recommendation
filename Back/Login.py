from flask import Flask, request, jsonify
from flask_login import current_user, LoginManager, login_user, logout_user, login_required, UserMixin
from model.dao import DAO

app = Flask(__name__)
app.secret_key = 'digite aqui sua chave secreta ou adicione um token seguro'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
   id_usuario = 0
   cpf_usuario = ''
   nome_usuario = ''
   email_usuario = ''

   def to_json(self):
       return {
           "id_usuario": self.id_usuario,
           "nome_usuario": self.nome_usuario,
           "email_usuario": self.email_usuario}

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
       return usr
   else:
       return None


# Tela inicial
@app.route('/homePage')


# Inserir novo usuário (cadastro de login)
@app.route('/createAcc', methods=['PUT'])
def inserir():
   daoUsr = DAO('tb_usuario')
   objUsr = daoUsr.tb_usuario()
   objUsr.nome_usuario = request.args.get('nome_usuario')
   objUsr.email_usuario = request.args.get('email_usuario')
   objUsr.senha_usuario = request.args.get('senha_usuario')

   daoUsr.create(objUsr)

   return jsonify({
       'id_usuario': objUsr.id_usuario,
   })


# Login do usuário
@app.route('/loginAcc', methods=['GET'])
def login():
   usuario = request.args.get('usuario')
   senha = request.args.get('senha')
   print(usuario, senha)
   dao = DAO('tb_usuario')
   lista = dao.readBy('nome_usuario', '==', usuario)
   if len(lista) == 1 and lista[0].senha_usuario:
       usr = User()
       usr.id_usuario = str(lista[0].id_usuario)
       usr.username = lista[0].nome_usuario
       usr.email_usuario = lista[0].email_usuario
       login_user(usr, remember=True)

       if current_user.is_authenticated:
           # Autentica o usuário novamente para que o método login_remembered() funcione corretamente
           return jsonify({
               'id_usuario': usr.id_usuario,
               'nome_usuario': usr.username,
               'email_usuario': usr.email_usuario
           })
   else:
       return jsonify({"status": 401,
                       "reason": "Erro de Login"})


# Tela de "Esqueceu senha"
@app.route('/senhaAcc', methods=['GET'])
# Pegar email da tabela usuário (?)


# Tela de logout (?)
@app.route('/logout', methods=['GET'])
def logout():
   logout_user()
   return jsonify(**{'result': 200,
                     'data': {'message': 'Logout feito com sucesso'}})


# Tela "inicial" pós login
@app.route('/start')
@login_required


if __name__ == "__main__":
   app.run(port=8080, debug=True)
