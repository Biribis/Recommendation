from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

class DAO:

   name = "root"
   password = "root"
   host = "localhost"
   database = "mydb"

   def __init__(self, tab):
       # Ligação com o esquema de banco de dados
       engine = create_engine("mysql+mysqlconnector://" + self.name + ":" + self.password + "@" + self.host + "/" + self.database + "?charset=utf8mb4") # arrumar com um endereço novo

       # Mapeamento Objeto Relacional com o SQLAlchemy
       db = automap_base()
       db.prepare(autoload_with=engine)
       self.tb_usuario = db.classes.tb_usuario
       self.tb_jogos = db.classes.tb_jogos
       self.tb_usuario_jogos = db.classes.tb_usuario_jogos

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

   def update(self):
       self.ses.commit()

   def delete(self, obj):
       self.ses.delete(obj)
       self.ses.commit()

   def getSes(self):
       return self.ses

   def __del__(self):
       self.ses.close()


if __name__ == '__main__':
   main()

