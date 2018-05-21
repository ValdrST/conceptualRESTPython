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
    registro = StringCol()
    cred_sem_carr_pln = MultipleJoin('cred_sem_carr_pln', joinColumn='cuenta')
    estudia_seriacion = MultipleJoin('estudia_seriacion', joinColumn='cuenta')
    bajas_temporales = MultipleJoin('bajas_temporales', joinColumn='cuenta')
    def _dir_alumnos_dgae(self):
        d = self.select()
        return d


class cred_sem_carr_pln(SQLObject):
    cuenta = ForeignKey('dir_alumnos_dgae')
    carrera = StringCol()
    pln = StringCol(name='pln')
    asem01 = StringCol(name='asem01')
    asem02 = StringCol()
    asem03 = StringCol()
    asem04 = StringCol()
    asem05 = StringCol()
    asem06 = StringCol()
    asem07 = StringCol()
    asem08 = StringCol()
    asem09 = StringCol()
    asem10 = StringCol()

class estudia_seriacion(SQLObject):
    carrera = StringCol()
    pln_dgae = StringCol()
    pln = StringCol()
    registro = StringCol()
    avance = StringCol()
    promedio = StringCol()
    creditos_cubiertos = StringCol()
    ultimo_cursado = StringCol()
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
    DAD = AliasTable(dir_alumnos_dgae,"DAD")
    P = AliasTable(periodo, "P")
    BT = AliasTable(bajas_temporales, "BT")
    CCP = AliasTable(cred_sem_carr_pln, "CCP")
    ES = AliasTable(estudia_seriacion,"ES")
    clave_carrera_dgae = AliasField(dir_alumnos_dgae, "carrera", "clave_carrera_dgae",DAD)
    clave_carrera_facultad = AliasField(estudia_seriacion, "carrera", "clave_carrera_facultad",ES)
    plan_dgae = AliasField(dir_alumnos_dgae, "plan_dgae","plan_dgae",DAD)
    plan_facultad = AliasField(estudia_seriacion,"pln","plan_facultad",ES)
    ultimoSemestre = AliasField(dir_alumnos_dgae,"registro","ultimo_semestre",DAD)
    #dir_alumnos_dgae.select(dir_alumnos_dgae.cuenta == id,join=LEFTJOINOn(ESTUDIA_SERIACION, dir_alumnos_dgae, len(dir_alumnos_dgae.cuenta)==9), join=LEFTJOINOn(bajas_temporales,CRED_SEM_CARR_PLN,ESTUDIA_SERIACION.PLN == CRED_SEM_CARR_PLN.PLN),dir_alumnos_dgae.PLAN_DGAE==ESTUDIA_SERIACION.pln_dgae,ESTUDIA_SERIACION.carrera==CRED_SEM_CARR_PLN.carrera)
    almn = dir_alumnos_dgae.selectBy(cuenta = '314144799')
    es = estudia_seriacion.selectBy(cuenta =  '314144799')
    ccp = cred_sem_carr_pln.selectBy(cuenta =  '314144799')
    ccp = ccp[0]
    alumno = almn[0]
    es = es[0]

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
    alumnos_generacion_carrera = estudia_seriacion.selectBy(registro = es.registro, carrera = es.carrera)
    alumnos_generacion_carrera = alumnos_generacion_carrera.count()
    alumnos_generacion = estudia_seriacion.selectBy(registro = es.registro)
    alumnos_generacion = alumnos_generacion.count()
    lugar_generacion = estudia_seriacion.selectBy(registro = es.registro, carrera = es.carrera)
    lugar_generacion = lugar_generacion.count()
    if((int(alumno.registro) - int(es.registro) % 10) == 0):
        lugar_carrera = (int(alumno.registro) - int(es.registro) / 10) - 1
    else:
        lugar_carrera = 2 * ((int(alumno.registro) - int(es.registro))/10) + 1
    if(lugar_carrera == 1):
        es2 = estudia_seriacion.select(estudia_seriacion.q.cuenta == alumno.cuenta, estudia_seriacion.q.pln == es.pln, estudia_seriacion.q.carrera == es.carrera, ccp.asem01>estudia_seriacion.q.avance)
        if (es2[0]):
            es2 = estudia_seriacion.select(estudia_seriacion.q.registro == es.registro, estudia_seriacion.q.creditos_cubiertos >= es.creditos_cubiertos, estudia_seriacion.q.promedio > es.promedio, estudia_seriacion.q.carrera == es.carrera).count()
        else:
            es2 = estudia_seriacion.select(estudia_seriacion.q.registro == es.registro, estudia_seriacion.q.creditos_cubiertos >= ccp.asem01, estudia_seriacion.q.promedio > es.promedio, estudia_seriacion.q.carrera == es.carrera).count()
    elif(lugar_carrera == 2):
        es2 = estudia_seriacion.select(estudia_seriacion.q.cuenta == alumno.cuenta, estudia_seriacion.q.pln == es.pln, estudia_seriacion.q.carrera == es.carrera, ccp.asem02>estudia_seriacion.q.avance)
        if (es2[0]):
            es2 = estudia_seriacion.select(estudia_seriacion.q.registro == es.registro, estudia_seriacion.q.creditos_cubiertos >= es.creditos_cubiertos, estudia_seriacion.q.promedio > es.promedio, estudia_seriacion.q.carrera == es.carrera).count()
        else:
            es2 = estudia_seriacion.select(estudia_seriacion.q.registro == es.registro, estudia_seriacion.q.creditos_cubiertos >= ccp.asem02, estudia_seriacion.q.promedio > es.promedio, estudia_seriacion.q.carrera == es.carrera).count()
    elif(lugar_carrera == 3):
            es2 = estudia_seriacion.select(estudia_seriacion.q.cuenta == alumno.cuenta, estudia_seriacion.q.pln == es.pln, estudia_seriacion.q.carrera == es.carrera, ccp.asem03>estudia_seriacion.q.avance)
            if (es2[0]):
                es2 = estudia_seriacion.select(estudia_seriacion.q.registro == es.registro, estudia_seriacion.q.creditos_cubiertos >= es.creditos_cubiertos, estudia_seriacion.q.promedio > es.promedio, estudia_seriacion.q.carrera == es.carrera).count()
            else:
                es2 = estudia_seriacion.select(estudia_seriacion.q.registro == es.registro, estudia_seriacion.q.creditos_cubiertos >= ccp.asem03, estudia_seriacion.q.promedio > es.promedio, estudia_seriacion.q.carrera == es.carrera).count()
    elif(lugar_carrera == 4):
        es2 = estudia_seriacion.select(estudia_seriacion.q.cuenta == alumno.cuenta, estudia_seriacion.q.pln == es.pln, estudia_seriacion.q.carrera == es.carrera, ccp.asem04>estudia_seriacion.q.avance)
        if (es2[0]):
            es2 = estudia_seriacion.select(estudia_seriacion.q.registro == es.registro, estudia_seriacion.q.creditos_cubiertos >= es.creditos_cubiertos, estudia_seriacion.q.promedio > es.promedio, estudia_seriacion.q.carrera == es.carrera).count()
        else:
            es2 = estudia_seriacion.select(estudia_seriacion.q.registro == es.registro, estudia_seriacion.q.creditos_cubiertos >= ccp.asem04, estudia_seriacion.q.promedio > es.promedio, estudia_seriacion.q.carrera == es.carrera).count()
    elif(lugar_carrera == 5):
        es2 = estudia_seriacion.select(estudia_seriacion.q.cuenta == alumno.cuenta, estudia_seriacion.q.pln == es.pln, estudia_seriacion.q.carrera == es.carrera, ccp.asem05>estudia_seriacion.q.avance)
        if (es2[0]):
            es2 = estudia_seriacion.select(estudia_seriacion.q.registro == es.registro, estudia_seriacion.q.creditos_cubiertos >= es.creditos_cubiertos, estudia_seriacion.q.promedio > es.promedio, estudia_seriacion.q.carrera == es.carrera).count()
        else:
            es2 = estudia_seriacion.select(estudia_seriacion.q.registro == es.registro, estudia_seriacion.q.creditos_cubiertos >= ccp.asem05, estudia_seriacion.q.promedio > es.promedio, estudia_seriacion.q.carrera == es.carrera).count()
    elif(lugar_carrera == 6):
        es2 = estudia_seriacion.select(estudia_seriacion.q.cuenta == alumno.cuenta, estudia_seriacion.q.pln == es.pln, estudia_seriacion.q.carrera == es.carrera, ccp.asem06>estudia_seriacion.q.avance)
        if (es2[0]):
            es2 = estudia_seriacion.select(estudia_seriacion.q.registro == es.registro, estudia_seriacion.q.creditos_cubiertos >= es.creditos_cubiertos, estudia_seriacion.q.promedio > es.promedio, estudia_seriacion.q.carrera == es.carrera).count()
        else:
            es2 = estudia_seriacion.select(estudia_seriacion.q.registro == es.registro, estudia_seriacion.q.creditos_cubiertos >= ccp.asem06, estudia_seriacion.q.promedio > es.promedio, estudia_seriacion.q.carrera == es.carrera).count()
    elif(lugar_carrera == 7):
        es2 = estudia_seriacion.select(estudia_seriacion.q.cuenta == alumno.cuenta, estudia_seriacion.q.pln == es.pln, estudia_seriacion.q.carrera == es.carrera, ccp.asem07>estudia_seriacion.q.avance)
        if (es2[0]):
            es2 = estudia_seriacion.select(estudia_seriacion.q.registro == es.registro, estudia_seriacion.q.creditos_cubiertos >= es.creditos_cubiertos, estudia_seriacion.q.promedio > es.promedio, estudia_seriacion.q.carrera == es.carrera).count()
        else:
            es2 = estudia_seriacion.select(estudia_seriacion.q.registro == es.registro, estudia_seriacion.q.creditos_cubiertos >= ccp.asem07, estudia_seriacion.q.promedio > es.promedio, estudia_seriacion.q.carrera == es.carrera).count()
    elif(lugar_carrera == 8):
        es2 = estudia_seriacion.select(estudia_seriacion.q.cuenta == alumno.cuenta, estudia_seriacion.q.pln == es.pln, estudia_seriacion.q.carrera == es.carrera, ccp.asem08>estudia_seriacion.q.avance)
        if (es2[0]):
            es2 = estudia_seriacion.select(estudia_seriacion.q.registro == es.registro, estudia_seriacion.q.creditos_cubiertos >= es.creditos_cubiertos, estudia_seriacion.q.promedio > es.promedio, estudia_seriacion.q.carrera == es.carrera).count()
        else:
            es2 = estudia_seriacion.select(estudia_seriacion.q.registro == es.registro, estudia_seriacion.q.creditos_cubiertos >= ccp.asem08, estudia_seriacion.q.promedio > es.promedio, estudia_seriacion.q.carrera == es.carrera).count()
    elif(lugar_carrera == 9):
        es2 = estudia_seriacion.select(estudia_seriacion.q.cuenta == alumno.cuenta, estudia_seriacion.q.pln == es.pln, estudia_seriacion.q.carrera == es.carrera, ccp.asem09>estudia_seriacion.q.avance)
        if (es2[0]):
            es2 = estudia_seriacion.select(estudia_seriacion.q.registro == es.registro, estudia_seriacion.q.creditos_cubiertos >= es.creditos_cubiertos, estudia_seriacion.q.promedio > es.promedio, estudia_seriacion.q.carrera == es.carrera).count()
        else:
            es2 = estudia_seriacion.select(estudia_seriacion.q.registro == es.registro, estudia_seriacion.q.creditos_cubiertos >= ccp.asem09, estudia_seriacion.q.promedio > es.promedio, estudia_seriacion.q.carrera == es.carrera).count()
    else:
        es2 = estudia_seriacion.select()
        #es2 = estudia_seriacion.select(estudia_seriacion.q.cuenta == alumno.cuenta, estudia_seriacion.q.pln == es.pln, estudia_seriacion.q.carrera == es.carrera, ccp.asem10 > estudia_seriacion.q.avance)
        if (es2[0]):
            es2 = estudia_seriacion.select()
            #es2 = estudia_seriacion.select(estudia_seriacion.q.registro == es.registro, estudia_seriacion.q.creditos_cubiertos >= es.creditos_cubiertos, estudia_seriacion.q.promedio > es.promedio, estudia_seriacion.q.carrera == es.carrera).count
        else:
            es2 = estudia_seriacion.select()
            #es2 = estudia_seriacion.select(estudia_seriacion.q.registro == es.registro, estudia_seriacion.q.creditos_cubiertos >= ccp.asem10, estudia_seriacion.q.promedio > es.promedio, estudia_seriacion.q.carrera == es.carrera).count()
    #lugar_generacion = estudia_seriacion.selectBy(cuenta = alumno.cuenta, pln = es.pln , carrera = es.carrera, avance = avance >=100)
    lugar_carrera = es2.count()
    return jsonify({'semestre_actual':semestre_actual,'clave_carrera_dgae':alumno.carrera,'clave_carrera_facultad':es.carrera,'plan_dgae':alumno.plan_dgae,'plan_facultad':es.pln,'semestre_registro':es.registro,'ultimo_semestre':alumno.registro,'semestre_calculo':semestre_calculo,'creditos_esperados':creditos_esperados,'alumnos_generacion_carrera':alumnos_generacion_carrera,'lugar_generacion':lugar_generacion,'lugar_carrera':lugar_carrera, 'promedio':es.promedio, 'creditos_cubiertos':es.creditos_cubiertos})
    
    

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
