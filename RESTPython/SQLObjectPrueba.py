from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlobject import *
from json import dumps
from sqlobject.sqlbuilder import *

sqlhub.processConnection = connectionForURI('mysql://valdr:nomad123@localhost:3306/pruebasy?charset=utf8')
app = Flask(__name__)
api = Api(app)

class dir_alumnos_dgae(SQLObject):
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


class cred_sem_carr_pln(SQLObject):
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

class ESTUDIA_SERIACION(SQLObject):
    carrera = StringCol()
    pln_dgae = StringCol()
    PLN = StringCol()
    REGISTRO = StringCol()
    AVANCE = StringCol()
    PROMEDIO = StringCol()
    CREDITOS_CUBIERTOS = StringCol()
    ULTIMO_CURSADO = StringCol()
    cuenta = ForeignKey('dir_alumnos_dgae')

class periodo(SQLObject):
    anio = StringCol()
    semestre = StringCol()

class bajas_temporales(SQLObject):
    cuenta = ForeignKey('dir_alumnos_dgae')


@app.route('/ranking/<id>', methods=['GET'])
def getRanking(id):
    p = periodo.select()
    for semestre_actual in p:
        semestre_actual = semestre_actual.anio + semestre_actual.semestre
    
    #dir_alumnos_dgae.select(dir_alumnos_dgae.cuenta == id,join=LEFTJOINOn(ESTUDIA_SERIACION, dir_alumnos_dgae, len(dir_alumnos_dgae.cuenta)==9), join=LEFTJOINOn(bajas_temporales,CRED_SEM_CARR_PLN,ESTUDIA_SERIACION.PLN == CRED_SEM_CARR_PLN.PLN),dir_alumnos_dgae.PLAN_DGAE==ESTUDIA_SERIACION.pln_dgae,ESTUDIA_SERIACION.carrera==CRED_SEM_CARR_PLN.carrera)    
    
    almn = dir_alumnos_dgae.selectBy(cuenta ='314144799')
    alumno = almn[0].cuenta
    return alumno
    
    

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
