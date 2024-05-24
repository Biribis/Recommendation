from sqlalchemy import create_engine, desc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

class DAO:

   name = "root"
   password = "quemleumecomeu"
   host = "localhost"
   database = "Recommendation"

   def __init__(self, tab):
       # Ligação com o esquema de banco de dados
       engine = create_engine("mysql+mysqlconnector://" + self.name + ":" + self.password + "@" + self.host + "/" + self.database + "?charset=utf8mb4") # arrumar com um endereço novo

       # Mapeamento Objeto Relacional com o SQLAlchemy
       db = automap_base()
       db.prepare(autoload_with=engine)
       self.tb_usuario = db.classes.tb_usuario
       self.tb_jogos = db.classes.tb_jogos
       self.tb_usuario_jogos = db.classes.tb_usuario_jogos
       self.tb_genero = db.classes.tb_genero

       self.tabela = eval("db.classes." + tab)
       self.id = "id_" + tab[3:len(tab)]

       # Trabalho com sessões da base Objeto-Relacional
       session_factory = sessionmaker(bind=engine)
       self.ses = session_factory()
       # -------------------------------------------------------------------------------------------------

   def create(self, obj):
       self.ses.add(obj)
       self.ses.commit()

   def readAll(self):
       lista = self.ses.query(self.tabela).all()
       return lista

   def readById(self, id):
       exp = "self.tabela." + self.id + "==id"
       obj = self.ses.query(self.tabela).filter(eval(exp)).first()
       return obj

   def readBy(self, campo, oper, valor):

       if oper == "==":
           exp = "self.tabela." + campo + "==valor"
       elif oper == "ilike":
           exp = "self.tabela." + campo + ".ilike('%' + valor + '%')"
       else:
           exp = "self.tabela." + campo + oper + "valor"

       lista = self.ses.query(self.tabela).filter(eval(exp)).all()
       return lista

   def selectid(self, campo):
       lst = self.ses.query(getattr(self.tabela, campo)).order_by(desc(getattr(self.tabela, campo))).first()[0]
       return lst

   def deletelastid(self, campo, ultimo):
       self.ses.query(self.tabela).filter(getattr(self.tabela, campo) == ultimo).delete()
       self.ses.commit()

   def selectUsuJog(self, id_jogo, id_usuario):
       lst = self.ses.query(self.tabela).filter_by(jogos_id_fk=id_jogo, usuario_id_fk=id_usuario).first()
       return lst

   def altFavourite(self, id_jogo, id_usuario, valor):
       lst = self.ses.query(self.tabela).filter_by(jogos_id_fk=id_jogo, usuario_id_fk=id_usuario).first()
       lst.favorito = valor
       self.ses.commit()

   def altAvalia(self, id_usuario, id_jogo, valor):
       lst = self.ses.query(self.tabela).filter_by(jogos_id_fk=id_jogo, usuario_id_fk=id_usuario).first()
       lst.avalia = valor
       self.ses.commit()

   def update(self):
       self.ses.commit()

   def delete(self, obj):
       self.ses.delete(obj)
       self.ses.commit()

   def getSes(self):
       return self.ses

   def __del__(self):
       self.ses.close()



