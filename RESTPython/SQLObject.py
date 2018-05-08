from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlobject import *
from json import dumps

sqlhub.processConnection = connectionForURI('mysql://valdr:nomad123@localhost:3306/prueba1?charset=utf8')
app = Flask(__name__)
api = Api(app)

class Usuarios(SQLObject):
    usuario = StringCol()
    nombre = StringCol()
    apellido = StringCol()
    fecha_nacimiento = StringCol()
    status = StringCol()
    def _get_usuarios(self):
        p = self.select()
        return p


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
