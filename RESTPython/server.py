from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from json import dumps

db_connect = create_engine('mysql+mysqldb://valdr:nomad123@localhost:3306/prueba1?charset=utf8')
Session = sessionmaker(bind= db_connect)
session = Session()
Base = declarative_base()
app = Flask(__name__)
api = Api(app)

class Usuarios(Base):
    __tablename__='usuarios'
    id = Column(Integer, primary_key=True)
    usuario = Column(String)
    nombre = Column(String)
    apellido = Column(String)
    fecha_nacimiento = Column(String)
    status = Column(String)
    
    def __repr__(self):
        return "Usuarios(id='{self.id}',nombre='{self.nombre}',apellido='{self.apellido}',fecha_nacimiento='{self.fecha_nacimiento}',status='{self.status}')".format(self=self)

    def _get_usuarios(self):
        p = self.select()
        return p

@app.route('/user', methods=['GET'])
def getUser():
    query = session.query(Usuarios).all()
    print(query)
    result = []
    for user in query:
        result.append({'usuario':user.usuario, 'nombre':user.nombre, 'apellido':user.apellido, 'fecha_nacimiento': user.fecha_nacimiento, 'status': user.status})
    return jsonify({'data':result})
    
@app.route('/user', methods=['POST'])
def postUser():
    print(request.json)
    usuario = request.json['usuario']
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    fecha_nacimiento = request.json['fecha_nacimiento']
    status = request.json['status']
    p = Usuarios(usuario = usuario, nombre = nombre, apellido = apellido, fecha_nacimiento = fecha_nacimiento, status = status)
    session.add(p)
    session.commit()
    return jsonify({'status':'success'})
    
@app.route('/user/<id>', methods=['GET'])
def getUserId(id):
    query = session.query(Usuarios).filter(Usuarios.id==id).first()
    print(query)
    result = {'data':{'usuario':query.usuario, 'nombre':query.nombre, 'apellido':query.apellido, 'fecha_nacimiento': query.fecha_nacimiento, 'status': query.status}}
    print(result)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0')