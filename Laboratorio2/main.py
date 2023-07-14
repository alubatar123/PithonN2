import api as api
import ids as ids
import time
import os

Tipoproceso=""

def funciontiempo(funcion_parametro):
    start_time = time.time()
    def funcion_inside():
        funcion_parametro()        
        duration = time.time() - start_time
        result = (f"Los nombres se leen en **{duration}** seg(s) de forma <ins>*{Tipoproceso}*<ins>")
        escribeMD(result)
    return funcion_inside

def escribeMD(result):
    if (os.path.exists("Laboratorio2/resultados.md"))==False:
        with open ("Laboratorio2/resultados.md","a+") as archivo: 
            archivo.write("# Laboratorio 1\n")
            archivo.write("## Resultados\n")
            archivo.write("+"+result+"\n")
            archivo.close
    else:
        with open ("Laboratorio2/resultados.md","a+") as archivo:            
            archivo.write("+"+result+"\n")            
        archivo.close

#-------------Funcion Sync#-------------

@funciontiempo
def cuenta_nombres():
    global Tipoproceso
    Tipoproceso="Sincrona"
    for e in ids.ids:       
        #print(api.getOneUser(e)["name"]) 
        (api.getOneUser(e)["name"])      


#-------------Funcion Concurrente#-------------

cuenta_nombres()
