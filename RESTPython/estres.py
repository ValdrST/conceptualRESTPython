import requests
import threading
from multiprocessing import Queue
import time
import sys

def getj(n,f):
    try:
        inicio = time.time()
        r = requests.get('http://localhost:5000/ranking/314144799')
        
        fin = time.time()
        tiempo = fin-inicio
        f.write("exito,"+str(tiempo)+"\n")
        #print(str(n) + str(r.json()))
    except:
        
        fin = time.time()
        tiempo = fin-inicio
        f.write("fallo,"+str(tiempo)+"\n")

def main():
    f = open (sys.argv[1], "w")
    f.write("estado,tiempo\n")
    global exito, fallo
    exito, fallo  = 0, 0
    for i in range (3000):
        thread = threading.Thread(target=getj, args=(i,f))
        thread.start()
    thread.join()
    #for linea in f:
     #   if linea == "exito\n":
      #      exito = exito + 1
       # elif linea == "fallo\n":
        #    fallo = fallo + 1
    #print(str(exito)+" "+str(fallo))
main()
