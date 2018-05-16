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

class dir_alumnos_dgae(Base):
    cuenta = StringCol()
    carrera = StringCol()
    plan_dgae = StringCol()
    Registro = StringCol()
    cred_sem_carr_pln = MultipleJoin('cred_sem_carr_pln', joinColumn='cuenta')
    estudia_seriacion = MultipleJoin('estudia_seriacion', joinColumn='cuenta')
    bajas_temporales = MultipleJoin('bajas_temporales', joinColumn='cuenta')
    def _dir_alumnos_dgae(self):
        d = self.select()
        return d


class cred_sem_carr_pln(Base):
    cuenta = ForeignKey('dir_alumnos_dgae')
    carrera = StringCol()
    PLN = StringCol()
    ASEM01 = StringCol()
    ASEM02 = StringCol()
    ASEM03 = StringCol()
    ASEM04 = StringCol()
    ASEM05 = StringCol()
    ASEM06 = StringCol()
    ASEM07 = StringCol()
    ASEM08 = StringCol()
    ASEM09 = StringCol()
    ASEM10 = StringCol()

class ESTUDIA_SERIACION(Base):
    carrera = StringCol()
    pln_dgae = StringCol()
    PLN = StringCol()
    REGISTRO = StringCol()
    AVANCE = StringCol()
    PROMEDIO = StringCol()
    CREDITOS_CUBIERTOS = StringCol()
    ULTIMO_CURSADO = StringCol()
    cuenta = ForeignKey('dir_alumnos_dgae')

class periodo(Base):
    anio = StringCol()
    semestre = StringCol()

class bajas_temporales(Base):
    cuenta = ForeignKey('dir_alumnos_dgae')

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

@app.route("/user/<id>", methods=['DELETE'])
def deleteUserId(id):
    query = session.query(Usuarios)
    query = query.filter(Usuarios.id == id)
    user = query.one()
    session.delete(user)
    session.commit()
    return jsonify({'status':'success'})

@app.route("/user/<id>", methods=['PUT'])
def modificarUserId(id):
    query = session.query(Usuarios)
    user = query.filter(Usuarios.id == id).first()
    user.usuario = request.json['usuario']
    user.nombre = request.json['nombre']
    user.apellido = request.json['apellido']
    user.fecha_nacimiento = request.json['fecha_nacimiento']
    user.status = request.json['status']
    session.commit()
    return jsonify({'status':'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0')