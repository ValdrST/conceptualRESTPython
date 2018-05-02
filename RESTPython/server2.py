from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlobject import *
from json import dumps

sqlhub.processConnection = connectionForURI('mysql+mysqldb://root:nomad123@localhost:3306/prueba1?charset=utf8')

class Employees(SQLObject):
    usuario = StringCol()
    nombre = StringCol()
    apellido = StringCol()
    fecha_nacimiento = StringCol()
    status = StringCol()

    def _get_Employees(self):
        return Employees.select()
    
    def _set_Employee(self):


app = Flask(__name__)
api = Api(app)


@app.route('/user', methods=['GET'])
def getUser():
    conn = db_connect.connect()
    query = conn.execute("select * from employees")
    return {'employees': [i[0] for i in query.cursor.fetchall()]}
    
@app.route('/user', methods=['POST'])
def postUser():
    print(request.json)
    usuario = request.json['usuario']
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    fecha_nacimiento = request.json['fecha_nacimiento']
    status = request.json['status']
    p = Employees(usuario = usuario, nombre = nombre, apellido = apellido, fecha_nacimiento = fecha_nacimiento, status = status)
    return jsonify({'status':'success'})
    
@app.route('/user/<id>', methods=['GET'])
def getUserId(id):
    conn = db_connect.connect()
    query = Employees.selectBy(id=id)
    result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0')