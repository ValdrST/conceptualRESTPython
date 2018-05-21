from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from json import dumps

db_connect = create_engine('mysql+mysqldb://valdr:nomad123@localhost:3306/pruebasy?charset=utf8')
Session = sessionmaker(bind= db_connect)
session = Session()
Base = declarative_base()
app = Flask(__name__)
api = Api(app)

class dir_alumnos_dgae(Base):
    __tablename__ = 'dir_alumnos_dgae'
    cuenta = Column(String(45), primary_key=True)
    carrera = Column(String(45))
    plan_dgae = Column(String(45))
    registro = Column(String(45))
    cred_sem_carr_pln = relationship('cred_sem_carr_pln', backref="dir_alumnos_dgae")
    estudia_seriacion = relationship('estudia_seriacion', backref="dir_alumnos_dgae")
    bajas_temporales = relationship('bajas_temporales', backref="dir_alumnos_dgae")


class cred_sem_carr_pln(Base):
    __tablename__ = 'cred_sem_carr_pln'
    id = Column(Integer(), primary_key=True)
    cuenta = Column('cuenta_id',String(45), ForeignKey('dir_alumnos_dgae.cuenta'))
    carrera = Column(String(45))
    pln = Column(String(45))
    asem01 = Column(String(45))
    asem02 = Column(String(45))
    asem03 = Column(String(45))
    asem04 = Column(String(45))
    asem05 = Column(String(45))
    asem06 = Column(String(45))
    asem07 = Column(String(45))
    asem08 = Column(String(45))
    asem09 = Column(String(45))
    asem10 = Column(String(45))

class estudia_seriacion(Base):
    __tablename__ = 'estudia_seriacion'
    id = Column(Integer(), primary_key=True)
    carrera = Column(String(45))
    pln_dgae = Column(String(45))
    pln = Column(String(45))
    registro = Column(String(45))
    avance = Column(String(45))
    promedio = Column(String(45))
    creditos_cubiertos = Column(String(45))
    ultimo_cursado = Column(String(45))
    cuenta = Column('cuenta_id',String(45), ForeignKey('dir_alumnos_dgae.cuenta'))

class periodo(Base):
    __tablename__ = 'periodo'
    id = Column(Integer(), primary_key=True)
    anio = Column(String(45))
    semestre = Column(String(45))

class bajas_temporales(Base):
    __tablename__ = 'bajas_temporales'
    id = Column(Integer(), primary_key=True)
    cuenta = Column(String(45), ForeignKey('dir_alumnos_dgae.cuenta'))

@app.route('/ranking/<id>', methods=['GET'])
def getRanking(id):
    p = session.query(periodo)
    semestre_actual = p[0].anio + p[0].semestre
    almn = session.query(dir_alumnos_dgae).filter(dir_alumnos_dgae.cuenta==id)
    es = session.query(estudia_seriacion).filter(estudia_seriacion.cuenta==id)
    ccp = session.query(cred_sem_carr_pln).filter(cred_sem_carr_pln.cuenta==id)
    alumno = almn[0]
    es = es[0]
    ccp = ccp[0]
    ultimo_cursado = es.ultimo_cursado
    registro = es.registro
    if(ultimo_cursado==''):
        semestre_calculo = es.registro % 10
        if(semestre_calculo == 0):
            semestre_calculo = 2 * ((int(ultimo_cursado) - int(registro)) / 10 ) - 1
        if(semestre_calculo == -1):
            semestre_calculo = 0
    else:
        semestre_calculo = 2 * ((int(ultimo_cursado) - int(registro))/ 10) + 1
    if(ultimo_cursado != ''):
        creditos_esperados = (int(ultimo_cursado)-int(registro)) % 10
        if( creditos_esperados == 0 ):
            creditos_esperados = 2 * ((int(ultimo_cursado) - int(registro))/ 10) - 1
        else:
            creditos_esperados = 2 * ((int(ultimo_cursado) - int(registro))/ 10) + 1
        if ( creditos_esperados == 1):
            creditos_esperados = ccp.asem01
        elif ( creditos_esperados == 2):
            creditos_esperados = ccp.asem02
        elif ( creditos_esperados == 3):
            creditos_esperados = ccp.asem03
        elif ( creditos_esperados == 4):
            creditos_esperados = ccp.asem04
        elif ( creditos_esperados == 5):
            creditos_esperados = ccp.asem05
        elif ( creditos_esperados == 6):
            creditos_esperados = ccp.asem06
        elif ( creditos_esperados == 7):
            creditos_esperados = ccp.asem07
        elif ( creditos_esperados == 8):
            creditos_esperados = ccp.asem08
        elif ( creditos_esperados == 9):
            creditos_esperados = ccp.asem09
        else:
            creditos_esperados = ccp.asem10
    alumnos_generacion_carrera = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.carrera == es.carrera).count()
    alumnos_generacion = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro).count()
    lugar_generacion = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.carrera == es.carrera, estudia_seriacion.avance >= 100).count()
    if((int(alumno.registro) - int(es.registro) % 10) == 0):
        lugar_carrera = (int(alumno.registro) - int(es.registro) / 10) - 1
    else:
        lugar_carrera = 2 * ((int(alumno.registro) - int(es.registro))/10) + 1
    if(lugar_carrera == 1):
        es2 = session.query(estudia_seriacion).filter(estudia_seriacion.cuenta == alumno.cuenta, estudia_seriacion.pln == es.pln, estudia_seriacion.carrera == es.carrera, ccp.asem01>estudia_seriacion.avance)
        if (es2[0]):
            es2 = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.creditos_cubiertos >= es.creditos_cubiertos, estudia_seriacion.promedio > es.promedio, estudia_seriacion.carrera == es.carrera).count()
        else:
            es2 = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.creditos_cubiertos >= ccp.asem01, estudia_seriacion.promedio > es.promedio, estudia_seriacion.carrera == es.carrera).count()
    elif(lugar_carrera == 2):
        es2 = session.query(estudia_seriacion).filter(estudia_seriacion.cuenta == alumno.cuenta, estudia_seriacion.pln == es.pln, estudia_seriacion.carrera == es.carrera, ccp.asem02>estudia_seriacion.avance)
        if (es2[0]):
            es2 = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.creditos_cubiertos >= es.creditos_cubiertos, estudia_seriacion.promedio > es.promedio, estudia_seriacion.carrera == es.carrera).count()
        else:
            es2 = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.creditos_cubiertos >= ccp.asem02, estudia_seriacion.promedio > es.promedio, estudia_seriacion.carrera == es.carrera).count()
    elif(lugar_carrera == 3):
            es2 = session.query(estudia_seriacion).filter(estudia_seriacion.cuenta == alumno.cuenta, estudia_seriacion.pln == es.pln, estudia_seriacion.carrera == es.carrera, ccp.asem03>estudia_seriacion.avance)
            if (es2[0]):
                es2 = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.creditos_cubiertos >= es.creditos_cubiertos, estudia_seriacion.promedio > es.promedio, estudia_seriacion.carrera == es.carrera).count()
            else:
                es2 = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.creditos_cubiertos >= ccp.asem03, estudia_seriacion.promedio > es.promedio, estudia_seriacion.carrera == es.carrera).count()
    elif(lugar_carrera == 4):
        es2 = session.query(estudia_seriacion).filter(estudia_seriacion.cuenta == alumno.cuenta, estudia_seriacion.pln == es.pln, estudia_seriacion.carrera == es.carrera, ccp.asem04>estudia_seriacion.avance)
        if (es2[0]):
            es2 = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.creditos_cubiertos >= es.creditos_cubiertos, estudia_seriacion.promedio > es.promedio, estudia_seriacion.carrera == es.carrera).count()
        else:
            es2 = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.creditos_cubiertos >= ccp.asem04, estudia_seriacion.promedio > es.promedio, estudia_seriacion.carrera == es.carrera).count()
    elif(lugar_carrera == 5):
        es2 = session.query(estudia_seriacion).filter(estudia_seriacion.cuenta == alumno.cuenta, estudia_seriacion.pln == es.pln, estudia_seriacion.carrera == es.carrera, ccp.asem05>estudia_seriacion.avance)
        if (es2[0]):
            es2 = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.creditos_cubiertos >= es.creditos_cubiertos, estudia_seriacion.promedio > es.promedio, estudia_seriacion.carrera == es.carrera).count()
        else:
            es2 = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.creditos_cubiertos >= ccp.asem05, estudia_seriacion.promedio > es.promedio, estudia_seriacion.carrera == es.carrera).count()
    elif(lugar_carrera == 6):
        es2 = session.query(estudia_seriacion).filter(estudia_seriacion.cuenta == alumno.cuenta, estudia_seriacion.pln == es.pln, estudia_seriacion.carrera == es.carrera, ccp.asem06>estudia_seriacion.avance)
        if (es2[0]):
            es2 = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.creditos_cubiertos >= es.creditos_cubiertos, estudia_seriacion.promedio > es.promedio, estudia_seriacion.carrera == es.carrera).count()
        else:
            es2 = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.creditos_cubiertos >= ccp.asem06, estudia_seriacion.promedio > es.promedio, estudia_seriacion.carrera == es.carrera).count()
    elif(lugar_carrera == 7):
        es2 = session.query(estudia_seriacion).filter(estudia_seriacion.cuenta == alumno.cuenta, estudia_seriacion.pln == es.pln, estudia_seriacion.carrera == es.carrera, ccp.asem07>estudia_seriacion.avance)
        if (es2[0]):
            es2 = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.creditos_cubiertos >= es.creditos_cubiertos, estudia_seriacion.promedio > es.promedio, estudia_seriacion.carrera == es.carrera).count()
        else:
            es2 = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.creditos_cubiertos >= ccp.asem07, estudia_seriacion.promedio > es.promedio, estudia_seriacion.carrera == es.carrera).count()
    elif(lugar_carrera == 8):
        es2 = session.query(estudia_seriacion).filter(estudia_seriacion.cuenta == alumno.cuenta, estudia_seriacion.pln == es.pln, estudia_seriacion.carrera == es.carrera, ccp.asem08>estudia_seriacion.avance)
        if (es2[0]):
            es2 = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.creditos_cubiertos >= es.creditos_cubiertos, estudia_seriacion.promedio > es.promedio, estudia_seriacion.carrera == es.carrera).count()
        else:
            es2 = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.creditos_cubiertos >= ccp.asem08, estudia_seriacion.promedio > es.promedio, estudia_seriacion.carrera == es.carrera).count()
    elif(lugar_carrera == 9):
        es2 = session.query(estudia_seriacion).filter(estudia_seriacion.cuenta == alumno.cuenta, estudia_seriacion.pln == es.pln, estudia_seriacion.carrera == es.carrera, ccp.asem09>estudia_seriacion.avance)
        if (es2[0]):
            es2 = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.creditos_cubiertos >= es.creditos_cubiertos, estudia_seriacion.promedio > es.promedio, estudia_seriacion.carrera == es.carrera).count()
        else:
            es2 = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.creditos_cubiertos >= ccp.asem09, estudia_seriacion.promedio > es.promedio, estudia_seriacion.carrera == es.carrera).count()
    else:
        es2 = session.query(estudia_seriacion).filter(estudia_seriacion.cuenta == alumno.cuenta, estudia_seriacion.pln == es.pln, estudia_seriacion.carrera == es.carrera, ccp.asem10 > estudia_seriacion.avance)
        if (es2.count()>=1):
            #es2 = session.query(estudia_seriacion)
            es2 = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.creditos_cubiertos >= es.creditos_cubiertos, estudia_seriacion.promedio > es.promedio, estudia_seriacion.carrera == es.carrera).count
        else:
            es2 = session.query(estudia_seriacion).filter(estudia_seriacion.registro == es.registro, estudia_seriacion.creditos_cubiertos >= ccp.asem10, estudia_seriacion.promedio > es.promedio, estudia_seriacion.carrera == es.carrera).count()
    #lugar_generacion = estudia_seriacion.selectBy(cuenta = alumno.cuenta, pln = es.pln , carrera = es.carrera, avance = avance >=100)
    lugar_carrera = es2
    return jsonify({'semestre_actual':semestre_actual,'clave_carrera_dgae':alumno.carrera,'clave_carrera_facultad':es.carrera,'plan_dgae':alumno.plan_dgae,'plan_facultad':es.pln,'semestre_registro':es.registro,'ultimo_semestre':alumno.registro,'semestre_calculo':semestre_calculo,'creditos_esperados':creditos_esperados,'alumnos_generacion_carrera':alumnos_generacion_carrera,'lugar_generacion':lugar_generacion,'lugar_carrera':lugar_carrera, 'promedio':es.promedio, 'creditos_cubiertos':es.creditos_cubiertos})

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