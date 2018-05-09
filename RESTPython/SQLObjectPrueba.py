from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlobject import *
from json import dumps
from sqlobject.sqlbuilder import *

sqlhub.processConnection = connectionForURI('mysql://valdr:nomad123@localhost:3306/prueba2?charset=utf8')
app = Flask(__name__)
api = Api(app)

class DIR_ALUMNOS_DGAE(SQLObject):
    CUENTA = StringCol()
    CARRERA = StringCol()
    PLAN_DGAE = StringCol()
    REGISTRO = StringCol()
    CRED_SEM_CARR_PLN = MultipleJoin('CRED_SEM_CARR_PLN', joinColumn='CUENTA')
    ESTUDIA_SERIACION = MultipleJoin('ESTUDIA_SERIACION', joinColumn='CUENTA')
    BAJAS_TEMPORALES = MultipleJoin('BAJAS_TEMPORALES', joinColumn='CUENTA')


class CRED_SEM_CARR_PLN(SQLObject):
    CUENTA = ForeignKey('DIR_ALUMNOS_DGAE')
    CARRERA = StringCol()
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

class ESTUDIA_SERIACION(SQLObject):
    CARRERA = StringCol()
    PLN_DGAE = StringCol()
    PLN = StringCol()
    REGISTRO = StringCol()
    AVANCE = StringCol()
    PROMEDIO = StringCol()
    CREDITOS_CUBIERTOS = StringCol()
    ULTIMO_CURSADO = StringCol()
    CUENTA = ForeignKey('DIR_ALUMNOS_DGAE')

class PERIODO(SQLObject):
    ANIO = StringCol()
    SEMESTRE = StringCol()

class BAJAS_TEMPORALES(SQLObject):
    CUENTA = ForeignKey('DIR_ALUMNOS_DGAE')


@app.route('/ranking/<id>', methods=['GET'])
def getRanking(id):
    periodo = PERIODO.select()
    for semestre_actual in periodo:
        semestre_actual = semestre_actual.ANIO + semestre_actual.SEMESTRE
    
    DIR_ALUMNOS_DGAE.select(DIR_ALUMNOS_DGAE.CUENTA == id,join=LEFTJOINOn(ESTUDIA_SERIACION, DIR_ALUMNOS_DGAE, len(DIR_ALUMNOS_DGAE.CUENTA)==9), join=LEFTJOINOn(BAJAS_TEMPORALES,CRED_SEM_CARR_PLN,ESTUDIA_SERIACION.PLN == CRED_SEM_CARR_PLN.PLN),DIR_ALUMNOS_DGAE.PLAN_DGAE==ESTUDIA_SERIACION.PLN_DGAE,ESTUDIA_SERIACION.CARRERA==CRED_SEM_CARR_PLN.CARRERA)    
    alumn = DIR_ALUMNOS_DGAE.selectBy(CUENTA='314144799')
    

@app.route('/user', methods=['GET'])
def getUser():
    query = Usuarios.select()
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
    return jsonify({'status':'success'})
    
@app.route('/user/<id>', methods=['GET'])
def getUserId(id):
    users = Usuarios.selectBy(id=id)
    for user in users:
        print("USUARIO"+str(user))
        result = {'data':{'usuario':user.usuario, 'nombre':user.nombre, 'apellido':user.apellido, 'fecha_nacimiento': user.fecha_nacimiento, 'status': user.status}}
        print(result)
        return jsonify(result)
    return jsonify({'status':'failed'})

@app.route("/user/<id>", methods=['DELETE'])
def deleteUserId(id):
    user = Usuarios.selectBy(id=id)[0]
    Usuarios.delete(user.id)
    return jsonify({'status':'success'})

@app.route("/user/<id>", methods=['PUT'])
def modificarUserId(id):
    user = Usuarios.selectBy(id=id)
    user[0].usuario = request.json['usuario']
    user[0].nombre = request.json['nombre']
    user[0].apellido = request.json['apellido']
    user[0].fecha_nacimiento = request.json['fecha_nacimiento']
    user[0].status = request.json['status']
    return jsonify({'status':'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
