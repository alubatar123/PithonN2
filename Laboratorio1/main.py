from datetime import datetime
from LabClase import Trig

cont=True #variable para saber si usuario desae continuar

def escribiendo(resultado):
        print(resultado)
        with open ("log.txt","a+") as archivo:
            archivo.write(str(datetime.now())+" "+resultado+"\n")            
            archivo.close

while cont:
    Pi_Objeto=Trig()
    print(" _____________________"'\n'
        "|    Bienvenido:      |"'\n'
        "|                     |"'\n'
        "| (1) Seno            |"'\n'
        "| (2) Coseno          |"'\n'
        "| (3) Tangente        |"'\n'
        "| (4) Salir           |"'\n'
        "|_____________________|"'\n')     
       
    operaracion=input("¿Que operacion desea realizar? ")
    if operaracion == "1":
         x=Pi_Objeto.Calcu_Seno()
         escribiendo(x)         
    elif operaracion == "2":
         x=(Pi_Objeto.Calcu_Coseno())
         escribiendo(x)         
    elif operaracion == "3":
         x=(Pi_Objeto.Calcu_Tangente())
         escribiendo(x)         
    elif operaracion == "4":
          cont = False  
    else:
         print("Seleccion invalida")      


