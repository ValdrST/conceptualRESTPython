from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

db_connect = create_engine('mysql+mysqldb://root:nomad123@localhost:3306/prueba1?charset=utf8')
app = Flask(__name__)
api = Api(app)


@app.route('/user', methods=['GET'])
def getUser(self):
    conn = db_connect.connect() # connect to database
    query = conn.execute("select * from employees") # This line performs query and returns json result
    return {'employees': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID
    
@app.route('/user', methods=['POST'])
def postUser(self):
    conn = db_connect.connect()
    print(request.json)
    LastName = request.json['LastName']
    FirstName = request.json['FirstName']
    Title = request.json['Title']
    ReportsTo = request.json['ReportsTo']
    BirthDate = request.json['BirthDate']
    HireDate = request.json['HireDate']
    Address = request.json['Address']
    City = request.json['City']
    State = request.json['State']
    Country = request.json['Country']
    PostalCode = request.json['PostalCode']
    Phone = request.json['Phone']
    Fax = request.json['Fax']
    Email = request.json['Email']
    query = conn.execute("insert into employees values(null,'{0}','{1}','{2}','{3}', \
                            '{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}', \
                            '{13}')".format(LastName,FirstName,Title,
                            ReportsTo, BirthDate, HireDate, Address,
                            City, State, Country, PostalCode, Phone, Fax,
                            Email))
    return {'status':'success'}
    
@app.route('/user/<id>', methods=['GET'])
def getUserId(id):
    conn = db_connect.connect()
    query = conn.execute("select * from employees where id =%d "  %int(id))
    result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0')