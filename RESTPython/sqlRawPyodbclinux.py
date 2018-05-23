from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps
import pyodbc
import time

app = Flask(__name__)
api = Api(app)

DB_HOST = 'http://localhost' 
DB_USER = 'valdr' 
DB_PASS = 'nomad123' 
DB_NAME = 'pruebasy'

def run_query(query=''):
    ConnectionString = "DSN=pruebasy;UID=valdr;PWD=nomad123"
    conn = pyodbc.connect(ConnectionString)
    cursor = conn.cursor() 
    cursor.execute(query)

    if query.upper().startswith('SELECT'):
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
    else: 
        conn.commit()               
        results = None 
    results = results[0]
    cursor.close()                  
    conn.close()                   
    return results

@app.route('/ranking/<id>', methods=['GET'])
def getRanking(id):
    try:
        return jsonify({'data':run_query(query='SELECT P.anio+P.semestre AS semestre_actual, DAD.carrera AS clave_carrera_dgae, ES.carrera AS clave_carrera_facultad, DAD.plan_dgae AS plan_dgae, ES.pln AS plan_facultad, ES.registro AS semestre_registro, DAD.registro AS ultimo_semestre, (CASE ((CONVERT((CASE ES.ultimo_cursado WHEN \'\' THEN \'{}\' ELSE ES.ultimo_cursado END),INTEGER)-CONVERT(ES.registro,INTEGER)) % 10) WHEN 0 THEN CASE (2 * ((CONVERT((CASE ES.ultimo_cursado WHEN \'\' THEN \'{}\' ELSE ES.ultimo_cursado END),INTEGER)-CONVERT(ES.registro,INTEGER)) / 10))-1 WHEN -1 THEN 0 ELSE (2 * ((CONVERT((CASE ES.ultimo_cursado WHEN \'\' THEN \'{}\' ELSE ES.ultimo_cursado END),INTEGER)-CONVERT(ES.registro,INTEGER)) / 10))-1 END ELSE 2 * (((CONVERT((CASE ES.ultimo_cursado WHEN \'\' THEN \'{}\' ELSE ES.ultimo_cursado END),INTEGER)-CONVERT(ES.registro,INTEGER)) / 10) + 1) END) AS semestre_calculo, ES.promedio AS promedio, ES.AVANCE AS avance, ES.CREDITOS_CUBIERTOS AS creditos_cubiertos, (CASE (CASE ((CONVERT((CASE ES.ultimo_cursado WHEN \'\' THEN \'{}\' ELSE ES.ultimo_cursado END),INTEGER)-CONVERT(ES.registro,INTEGER)) % 10) WHEN 0 THEN (2 * ((CONVERT((CASE ES.ultimo_cursado WHEN \'\' THEN \'{}\' ELSE ES.ultimo_cursado END),INTEGER)-CONVERT(ES.registro,INTEGER)) / 10))-1 ELSE 2 * (((CONVERT((CASE ES.ultimo_cursado WHEN \'\' THEN \'{}\' ELSE ES.ultimo_cursado END),INTEGER)-CONVERT(ES.registro,INTEGER)) / 10) + 1) END) WHEN -1 THEN 0 WHEN 1 THEN CCP.ASEM01 WHEN 2 THEN CCP.ASEM02 WHEN 3 THEN CCP.ASEM03 WHEN 4 THEN CCP.ASEM04 WHEN 5 THEN CCP.ASEM05 WHEN 6 THEN CCP.ASEM06 WHEN 7 THEN CCP.ASEM07 WHEN 8 THEN CCP.ASEM08 WHEN 9 THEN CCP.ASEM09 ELSE CCP.ASEM10 END) AS creditos_esperados, (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro) AS alumnos_generacion, (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.carrera=ES.carrera) AS alumnos_generacion_carrera, (CASE (SELECT 100 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND ES2.AVANCE>=100) WHEN 100 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.carrera=ES.carrera AND ES2.AVANCE>=100) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.carrera=ES.carrera AND ES2.AVANCE>=ES.AVANCE) END) AS lugar_generacion, (CASE (CASE ((CONVERT(DAD.registro,INTEGER)-CONVERT(ES.registro,INTEGER)) % 10) WHEN 0 THEN (2 * ((CONVERT(DAD.registro,INTEGER)-CONVERT(ES.registro,INTEGER)) / 10))-1 ELSE 2 * (((CONVERT(DAD.registro,INTEGER)-CONVERT(ES.registro,INTEGER)) / 10) + 1) END) WHEN 1 THEN (CASE (SELECT 1 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND CCP.ASEM01>ES2.AVANCE) WHEN 1 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=ES.CREDITOS_CUBIERTOS AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=CCP.ASEM01 AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) END) WHEN 2 THEN (CASE (SELECT 1 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND CCP.ASEM02>ES2.AVANCE) WHEN 1 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=ES.CREDITOS_CUBIERTOS AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=CCP.ASEM02 AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) END) WHEN 3 THEN (CASE (SELECT 1 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND CCP.ASEM03>ES2.AVANCE) WHEN 1 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=ES.CREDITOS_CUBIERTOS AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=CCP.ASEM03 AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) END) WHEN 4 THEN (CASE (SELECT 1 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND CCP.ASEM04>ES2.AVANCE) WHEN 1 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=ES.CREDITOS_CUBIERTOS AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=CCP.ASEM04 AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) END) WHEN 5 THEN (CASE (SELECT 1 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND CCP.ASEM05>ES2.AVANCE) WHEN 1 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=ES.CREDITOS_CUBIERTOS AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=CCP.ASEM05 AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) END) WHEN 6 THEN (CASE (SELECT 1 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND CCP.ASEM06>ES2.AVANCE) WHEN 1 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=ES.CREDITOS_CUBIERTOS AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=CCP.ASEM06 AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) END) WHEN 7 THEN (CASE (SELECT 1 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND CCP.ASEM07>ES2.AVANCE) WHEN 1 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=ES.CREDITOS_CUBIERTOS AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=CCP.ASEM07 AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) END) WHEN 8 THEN (CASE (SELECT 1 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND CCP.ASEM08>ES2.AVANCE) WHEN 1 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=ES.CREDITOS_CUBIERTOS AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=CCP.ASEM08 AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) END) WHEN 9 THEN (CASE (SELECT 1 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND CCP.ASEM09>ES2.AVANCE) WHEN 1 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=ES.CREDITOS_CUBIERTOS AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=CCP.ASEM09 AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) END) ELSE (CASE (SELECT 1 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND CCP.ASEM10>ES2.AVANCE) WHEN 1 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=ES.CREDITOS_CUBIERTOS AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=CCP.ASEM10 AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) END) END) AS lugar_carrera FROM periodo P, dir_alumnos_dgae DAD LEFT JOIN estudia_seriacion ES ON DAD.cuenta=RIGHT(\'000000000\'+ES.cuenta_ID,9) LEFT JOIN bajas_temporales BT ON DAD.cuenta=RIGHT(\'000000000\'+BT.cuenta,9) LEFT JOIN CRED_SEM_CARR_PLN CCP ON ES.pln=CCP.pln WHERE DAD.cuenta=\'314144799\' AND DAD.plan_dgae=ES.pln_dgae AND ES.carrera=CCP.carrera')})
    except:
        time.sleep(3)
        return jsonify({'data':run_query(query='SELECT P.anio+P.semestre AS semestre_actual, DAD.carrera AS clave_carrera_dgae, ES.carrera AS clave_carrera_facultad, DAD.plan_dgae AS plan_dgae, ES.pln AS plan_facultad, ES.registro AS semestre_registro, DAD.registro AS ultimo_semestre, (CASE ((CONVERT((CASE ES.ultimo_cursado WHEN \'\' THEN \'{}\' ELSE ES.ultimo_cursado END),INTEGER)-CONVERT(ES.registro,INTEGER)) % 10) WHEN 0 THEN CASE (2 * ((CONVERT((CASE ES.ultimo_cursado WHEN \'\' THEN \'{}\' ELSE ES.ultimo_cursado END),INTEGER)-CONVERT(ES.registro,INTEGER)) / 10))-1 WHEN -1 THEN 0 ELSE (2 * ((CONVERT((CASE ES.ultimo_cursado WHEN \'\' THEN \'{}\' ELSE ES.ultimo_cursado END),INTEGER)-CONVERT(ES.registro,INTEGER)) / 10))-1 END ELSE 2 * (((CONVERT((CASE ES.ultimo_cursado WHEN \'\' THEN \'{}\' ELSE ES.ultimo_cursado END),INTEGER)-CONVERT(ES.registro,INTEGER)) / 10) + 1) END) AS semestre_calculo, ES.promedio AS promedio, ES.AVANCE AS avance, ES.CREDITOS_CUBIERTOS AS creditos_cubiertos, (CASE (CASE ((CONVERT((CASE ES.ultimo_cursado WHEN \'\' THEN \'{}\' ELSE ES.ultimo_cursado END),INTEGER)-CONVERT(ES.registro,INTEGER)) % 10) WHEN 0 THEN (2 * ((CONVERT((CASE ES.ultimo_cursado WHEN \'\' THEN \'{}\' ELSE ES.ultimo_cursado END),INTEGER)-CONVERT(ES.registro,INTEGER)) / 10))-1 ELSE 2 * (((CONVERT((CASE ES.ultimo_cursado WHEN \'\' THEN \'{}\' ELSE ES.ultimo_cursado END),INTEGER)-CONVERT(ES.registro,INTEGER)) / 10) + 1) END) WHEN -1 THEN 0 WHEN 1 THEN CCP.ASEM01 WHEN 2 THEN CCP.ASEM02 WHEN 3 THEN CCP.ASEM03 WHEN 4 THEN CCP.ASEM04 WHEN 5 THEN CCP.ASEM05 WHEN 6 THEN CCP.ASEM06 WHEN 7 THEN CCP.ASEM07 WHEN 8 THEN CCP.ASEM08 WHEN 9 THEN CCP.ASEM09 ELSE CCP.ASEM10 END) AS creditos_esperados, (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro) AS alumnos_generacion, (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.carrera=ES.carrera) AS alumnos_generacion_carrera, (CASE (SELECT 100 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND ES2.AVANCE>=100) WHEN 100 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.carrera=ES.carrera AND ES2.AVANCE>=100) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.carrera=ES.carrera AND ES2.AVANCE>=ES.AVANCE) END) AS lugar_generacion, (CASE (CASE ((CONVERT(DAD.registro,INTEGER)-CONVERT(ES.registro,INTEGER)) % 10) WHEN 0 THEN (2 * ((CONVERT(DAD.registro,INTEGER)-CONVERT(ES.registro,INTEGER)) / 10))-1 ELSE 2 * (((CONVERT(DAD.registro,INTEGER)-CONVERT(ES.registro,INTEGER)) / 10) + 1) END) WHEN 1 THEN (CASE (SELECT 1 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND CCP.ASEM01>ES2.AVANCE) WHEN 1 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=ES.CREDITOS_CUBIERTOS AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=CCP.ASEM01 AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) END) WHEN 2 THEN (CASE (SELECT 1 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND CCP.ASEM02>ES2.AVANCE) WHEN 1 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=ES.CREDITOS_CUBIERTOS AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=CCP.ASEM02 AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) END) WHEN 3 THEN (CASE (SELECT 1 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND CCP.ASEM03>ES2.AVANCE) WHEN 1 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=ES.CREDITOS_CUBIERTOS AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=CCP.ASEM03 AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) END) WHEN 4 THEN (CASE (SELECT 1 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND CCP.ASEM04>ES2.AVANCE) WHEN 1 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=ES.CREDITOS_CUBIERTOS AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=CCP.ASEM04 AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) END) WHEN 5 THEN (CASE (SELECT 1 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND CCP.ASEM05>ES2.AVANCE) WHEN 1 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=ES.CREDITOS_CUBIERTOS AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=CCP.ASEM05 AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) END) WHEN 6 THEN (CASE (SELECT 1 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND CCP.ASEM06>ES2.AVANCE) WHEN 1 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=ES.CREDITOS_CUBIERTOS AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=CCP.ASEM06 AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) END) WHEN 7 THEN (CASE (SELECT 1 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND CCP.ASEM07>ES2.AVANCE) WHEN 1 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=ES.CREDITOS_CUBIERTOS AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=CCP.ASEM07 AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) END) WHEN 8 THEN (CASE (SELECT 1 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND CCP.ASEM08>ES2.AVANCE) WHEN 1 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=ES.CREDITOS_CUBIERTOS AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=CCP.ASEM08 AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) END) WHEN 9 THEN (CASE (SELECT 1 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND CCP.ASEM09>ES2.AVANCE) WHEN 1 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=ES.CREDITOS_CUBIERTOS AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=CCP.ASEM09 AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) END) ELSE (CASE (SELECT 1 FROM estudia_seriacion ES2 WHERE ES2.cuenta_ID=ES.cuenta_ID AND ES2.pln=ES.pln AND ES2.carrera=ES.carrera AND CCP.ASEM10>ES2.AVANCE) WHEN 1 THEN (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=ES.CREDITOS_CUBIERTOS AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) ELSE (SELECT COUNT(*) FROM estudia_seriacion ES2 WHERE ES2.registro=ES.registro AND ES2.CREDITOS_CUBIERTOS>=CCP.ASEM10 AND ES2.promedio>ES.promedio AND ES2.carrera=ES.carrera) END) END) AS lugar_carrera FROM periodo P, dir_alumnos_dgae DAD LEFT JOIN estudia_seriacion ES ON DAD.cuenta=RIGHT(\'000000000\'+ES.cuenta_ID,9) LEFT JOIN bajas_temporales BT ON DAD.cuenta=RIGHT(\'000000000\'+BT.cuenta,9) LEFT JOIN CRED_SEM_CARR_PLN CCP ON ES.pln=CCP.pln WHERE DAD.cuenta=\'314144799\' AND DAD.plan_dgae=ES.pln_dgae AND ES.carrera=CCP.carrera')})
         
if __name__ == '__main__':
    app.run(host='0.0.0.0')
