import requests
import threading
from multiprocessing import Queue
import time
import sys
from analisis import analisis

def getj(n,f):
    try:
        inicio = time.time()
        r = requests.get('http://localhost:5000/ranking/314144799')
        
        fin = time.time()
        tiempo = fin-inicio
        f.write("exito,"+str(tiempo)+"\n")
        #print(str(n) + str(r.json()))
    except Exception as inst:
        print(inst)
        print(type(inst))
        fin = time.time()
        tiempo = fin-inicio
        f.write("fallo,"+str(tiempo)+"\n")

def main():
    f = open (sys.argv[1], "w")
    f.write("estado,tiempo\n")
    global exito, fallo
    exito, fallo  = 0, 0
    for i in range (int(sys.argv[2])):
        thread = threading.Thread(target=getj, args=(i,f))
        thread.start()
    thread.join()
    analisis()

main()

