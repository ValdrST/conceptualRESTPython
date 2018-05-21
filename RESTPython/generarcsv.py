from random import randint
from csvtoinsert import generarSQL
def main():
    tablas = ['cred_sem_carr_pln.csv','dir_alumnos_dgae.csv','estudia_seriacion.csv','periodo.csv','bajas_temporales.csv']
    f1 = open("cred_sem_carr_pln.csv","w")
    f1.write("CUENTA_ID,ASEM01,ASEM02,ASEM03,ASEM04,ASEM05,ASEM06,ASEM07,ASEM08,ASEM09,ASEM10,CARRERA,PLN\n")
    cuenta = []
    for i in range(10000):
        cuenta.append(str(randint(100000000,499999999)))
    carrera = []
    for i in range(10000):
        carrera.append(str(randint(100,135)))
    plndgae = []
    for i in range(10000):
        plndgae.append(str(randint(1000,4000)))


    for i in range(10000):
        f1.write( str(cuenta[i]) + "," +  str(randint(0,20))+ "," +  str(randint(20,40))+ "," +  str(randint(40,60))+ "," +  str(randint(60,80))+ "," +  str(randint(80,100))+ "," +  str(randint(100,120))+ "," +  str(randint(120,140))+ "," +  str(randint(160,180))+ "," +  str(randint(200,220))+ "," +  str(randint(220,240))+"," + str(randint(100,135)) + "," +str(randint(2000,2016))+"\n")
    f1.close()
    f1 = open('dir_alumnos_dgae.csv',"w")
    f1.write("CUENTA,CARRERA,PLAN_DGAE,REGISTRO\n")
    for i in range(10000):
        f1.write( str(cuenta[i]) + "," + str(carrera[i]) + "," + str(plndgae[i]) + "," + str(randint(1,10))+"\n")
    f1.close()
    f1 =open('estudia_seriacion.csv',"w")
    f1.write("CUENTA_ID,CARRERA,PLN_DGAE,PLN,REGISTRO,AVANCE,PROMEDIO,CREDITOS_CUBIERTOS,ULTIMO_CURSADO\n")
    for i in range(10000):
        f1.write(str(cuenta[i]) + "," + str(carrera[i]) + "," + str(plndgae[i])+","+str(randint(2000,2016))+","+str(randint(1,10))+","+str(randint(1,200))+","+str(randint(5,10))+","+str(randint(1,200))+","+str(randint(1,10))+"\n")
    f1.close()
    f1 = open('bajas_temporales.csv',"w")
    f1.write("CUENTA,SEMESTRE\n")
    for i in range(10000):
        f1.write(str(cuenta[i])+","+str(randint(2,10))+"\n")
    f1.close()
    tablas = ['cred_sem_carr_pln.csv','dir_alumnos_dgae.csv','estudia_seriacion.csv','bajas_temporales.csv']
    generarSQL(tablas)

main()

