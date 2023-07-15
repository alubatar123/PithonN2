import api as api
import ids as ids
import time
import os
import concurrent.futures
import multiprocessing
import asyncio


Tipoproceso=""

#Funcion decoradora para calcular el tiempo de demara
def funciontiempo(funcion_parametro):
    start_time = time.time()
    def funcion_inside(*args):
        funcion_parametro(*args)     
        duration = time.time() - start_time
        result = (f"Los nombres se leen en **{duration}** seg(s) de forma *{Tipoproceso}*<br /> ")
        escribeMD(result)
    return funcion_inside

#funcion que permite escribir los resultado a un .md file
def escribeMD(result):
    if (os.path.exists("Laboratorio2/resultados.md"))==False:
        #se verifica si el archivo ya existe
        with open ("Laboratorio2/resultados.md","a+") as archivo: 
            archivo.write("# Laboratorio 2\n ")
            archivo.write("## Conclusion \n ")
            archivo.write("> El uso de threads fue el que mejor resultado presento. Seguido por el multiproceso. AsyncIO no mostro mejorias al no haber multiples tareas ejecutandose.<br/>\n ")
            archivo.write("#### Resultados\n ")            
            archivo.write("+"+result)
            archivo.close
    else:
        with open ("Laboratorio2/resultados.md","a+") as archivo:            
            archivo.write("+"+result)            
            archivo.close



#-------------------------------------- 
#-------------Funcion Sync-------------
#--------------------------------------

"""

#Funcion Synch que obtiene los nombres del diccionario
@funciontiempo
def cuenta_nombres():
    global Tipoproceso
    Tipoproceso="Sync"
    for e in ids.ids:       
        print(api.getOneUser(e)["name"]) 
        #(api.getOneUser(e)["name"])      

#cuenta_nombres()


"""

#----------------------------------------- 
#-------------Funcion Threads-------------
#----------------------------------------- 




def cuenta_nombres_thread(ListID):
    global Tipoproceso
    Tipoproceso="Threads"         
    print(api.getOneUser(ListID)["name"]) 
    #api.getOneUser(ListID)["name"]
         

@funciontiempo
def usando_thread():
    #Mediante maps se relacionan los contenidos de la lista y la funcion mediante hilos
    with concurrent.futures.ThreadPoolExecutor() as MyExecutor:
        MyExecutor.map(cuenta_nombres_thread,ids.ids)
    
usando_thread()





#----------------------------------------- 
#-----------Funcion Multiprocess----------
#----------------------------------------- 

"""


def cuenta_nombres_Multi(ListID):           
    print(api.getOneUser(ListID)["name"]) 
    #api.getOneUser(ListID)["name"]    

@funciontiempo
def crear_pool(MiLista):
    global Tipoproceso
    Tipoproceso="Multiprocess"
    #Mediante maps se relacionan los contenidos de la lista y la funcion mediante multiprocesos     
    with multiprocessing.Pool() as pool:       
        pool.map(cuenta_nombres_Multi, MiLista)
           

if __name__ == "__main__":              
        crear_pool(ids.ids)         

"""        


#-----------------------------------------    
#-------------Funcion AsyncIO-------------
#-----------------------------------------
"""
async def cuenta_nombres_Multi(ListaID):           
    print(api.getOneUser(ListaID)["name"]) 


async def main():
    start_time = time.time()      
    
    list=[]
    for id in ids.ids:
        list.append(cuenta_nombres_Multi(id))
    await asyncio.gather(*list)
    duration = time.time() - start_time

    #se escriben los resultados al archivo .md
    result = (f"Los nombres se leen en **{duration}** seg(s) de forma *AsynchIO*<br /> ")   

    with open ("Laboratorio2/resultados.md","a+") as archivo:            
            archivo.write("+"+result)            
            archivo.close         


asyncio.run(main())    
"""


