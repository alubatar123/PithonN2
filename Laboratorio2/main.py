import api as api
import ids as ids
import time
import os
import concurrent.futures
import multiprocessing
import asyncio


Tipoproceso=""

def funciontiempo(funcion_parametro):
    start_time = time.time()
    def funcion_inside(*args):
        funcion_parametro(*args)     
        duration = time.time() - start_time
        result = (f"Los nombres se leen en **{duration}** seg(s) de forma *{Tipoproceso}*<br /> ")
        escribeMD(result)
    return funcion_inside

def escribeMD(result):
    if (os.path.exists("Laboratorio2/resultados.md"))==False:
        with open ("Laboratorio2/resultados.md","a+") as archivo: 
            archivo.write("# Laboratorio 1\n")
            archivo.write("## Resultados\n")
            archivo.write("+"+result)
            archivo.close
    else:
        with open ("Laboratorio2/resultados.md","a+") as archivo:            
            archivo.write("+"+result)            
            archivo.close

#-------------Funcion Sync#-------------


@funciontiempo
def cuenta_nombres():
    global Tipoproceso
    Tipoproceso="Sync"
    for e in ids.ids:       
        #print(api.getOneUser(e)["name"]) 
        (api.getOneUser(e)["name"])      

cuenta_nombres()
#-------------Funcion Threads#-------------

def cuenta_nombres_thread(NameList):
    global Tipoproceso
    Tipoproceso="Threads"         
    #print(api.getOneUser(NameList)["name"]) 
    api.getOneUser(NameList)["name"]
         

@funciontiempo
def usando_thread():
    with concurrent.futures.ThreadPoolExecutor() as MyExecutor:
        MyExecutor.map(cuenta_nombres_thread,ids.ids)
    
usando_thread()

#-------------Funcion Multiprocess#-------------


def cuenta_nombres_Multi(ListaNum):           
    #print(api.getOneUser(ListaNum)["name"]) 
    api.getOneUser(ListaNum)["name"]    

@funciontiempo
def crear_pool(MiLista):
    global Tipoproceso
    Tipoproceso="Multiprocess"     
    with multiprocessing.Pool() as pool:       
        pool.map(cuenta_nombres_Multi, MiLista)
           

#if __name__ == "__main__":              
  #      crear_pool(ids.ids)         

     
#-------------Funcion AsyncIO-------------
async def cuenta_nombres_Multi(ListaNum):           
    print(api.getOneUser(ListaNum)["name"]) 

@funciontiempo
async def main():
    global Tipoproceso
    Tipoproceso="Sync"
    print("start") 
    list=[]
    for i in ids.ids:
        list.append(cuenta_nombres_Multi(i))  
    await asyncio.gather(*list)
    print("done")              

#asyncio.run(main())    



