import requests
import time
cont=True
"""
 La API escogida proviene de https://ygoprodeck.com/api-guide/ la cual proporciona una base
 de datos de diferentes estadisticas de cada carta de Yu-Gi-Oh asi como sus caracteristicas.
  Los metodos creados permiten filtrar por algunas de las subcategorias asi como ver
 estadisticas por carta.
  Actualmente existen 12,456 cartas, por lo que se limitó la cantidad de valores a imprimir. 
 
"""
#funcion para filtrar tipos de datos de la base de datos principal
def GetData(url,filter):    
    getResponse = requests.get(url)  
    if getResponse.status_code == 200:
        data= getResponse.json()               
    for elem in data["data"]:    
        try:
            if elem['level']!=None:
                yield (elem[filter])  #almacena las raza en el Set
        except KeyError:
            pass    
          

#funcion para cambiar el ancho de las columnas
def GetLength(url,filter):
    print("Processing request...")
    MyIterator =GetData(url,filter)
    TempSet=set()#quitamos datos repetidos
    lenght=1
    for elem in MyIterator:
         TempSet.add(elem)
         if len(elem)>lenght:
             lenght=len(elem) #se ajusta el largo a la carta con mas letras
    return lenght, sorted(list(TempSet))        
     #TempSet=#ordena Set


def Gettype(): #Funcion que filtra los tipos de cartas
    lenght,newlist= GetLength("https://db.ygoprodeck.com/api/v7/cardinfo.php","type")
        
    print("\n • LIST OF CARD TYPES\n")

    #se imprimen los elementos em pares
    for elem in range(len(newlist)):
        if elem<9: #agrega un espacio para numeros de 1 digito
            print("( ",elem+1,")", newlist[elem]," "*(lenght-len(newlist[elem])),end="")
        else:
            print("(",elem+1,")", newlist[elem]," "*(lenght-len(newlist[elem])),end="")    
        if (elem+1)%2==0: #cada dos resultado hace salto de linea
            print()
    print()

#funcion para imprimir atributos de las cartas
def GetAttribute():
    lenght,newlist= GetLength("https://db.ygoprodeck.com/api/v7/cardinfo.php","attribute")
        
    print("\n • LIST OF CARD ATTRIBUTES\n")

    #se imprimen los elementos en grupos
    for elem in range(len(newlist)):
            print("(",elem+1,")", newlist[elem]," "*(lenght-len(newlist[elem])),end="")    
            if (elem+1)%4==0:# cada 4 resultados hace salto de linea
                print()
    print()

#funcion para imprimir razas de las cartas
def Getrace():
    lenght,newlist= GetLength("https://db.ygoprodeck.com/api/v7/cardinfo.php?sort=level","race")
    for e in newlist:#Algunas cartas no tienen raza, por lo que se remueven valores vacios
         if len(e)<2:
            newlist.remove(e)

    print("\n • LIST OF CARD RACES\n")   
    #se imprimen los elementos en cuartetos    
    for elem in range(len(newlist)):        
        if elem<9:#agrega un espacio para numeros de 1 digito
            print("( ",elem+1,")", newlist[elem]," "*(lenght-len(newlist[elem])),end="")
        else:
            print("(",elem+1,")", newlist[elem]," "*(lenght-len(newlist[elem])),end="")
        if (elem+1)%4==0:# cada 4 resultados hace salto de linea
            print()    
    print()    
    
#funcion que permite filtrar por tipo, raza o atributo
def FilterFunc(Filter):
    Select=input(f"\nEnter the name of the {Filter} to filter: ('quit' to return) ")
    if Select.lower() == "quit":
        pass
    else:
        try:
            getResponse = requests.get(f'https://db.ygoprodeck.com/api/v7/cardinfo.php?{Filter}={Select.upper()}')
            
            if getResponse.status_code == 200:
                data= getResponse.json()
            counter=0
            TempDic={}
            #Filtra datos y los almacena en Dicc temporal
            for elem in data["data"]:            
                    try:
                        if elem['level']!=None:
                            TempDic[counter]=[str(elem['id']),
                                            (elem['name'][:28] if len(elem['name']) > 28 else elem['name']), #Max largo de nombre = 37 letras
                                            elem['type'],elem['race'],str(elem['attribute'])]
                        counter+=1    
                        
                    except KeyError:
                        pass
            PrintFilterData(TempDic)
            Next()
        except:
            print("-Incorrect Value or filter does not exists")
            print(" Returning  to main menu\n") 
            time.sleep(2) 

#funcion que imprime los datos filtrados
def PrintFilterData(TempDic):
    print("Processing request...")
    time.sleep(2)
    tablelengh=[6,8,8,9,9] #lista para el largo de columnas
    for elem in TempDic.values():#modifica el largo de las columnas de ser necesario        
            for i in range(len(tablelengh)):               
               if len(elem[i]) > tablelengh[i]:
                    tablelengh[i] = len(elem[i])            
    
    Margen=("="*(sum(list(filter(lambda x : (x),tablelengh)))+16))#linea del largo de valores
    print(Margen)
    print("|   ID"," "*(tablelengh[0]-5),"|   NAME"," "*(tablelengh[1]-7),
          "|   TYPE"," "*(tablelengh[2]-7),"|   RACE"," "*(tablelengh[3]-7),"| ATTRIBUTE |")
    print(Margen)
    
    MaxElem=1
    for elem in TempDic.values(): 
        if MaxElem<50:  #se limita a 30 resultados ya que la base de datos es enorme           
                for e in range(len(elem)):                    
                    print(f'| {elem[e]+" "*(tablelengh[e]-len(elem[e]))} ',end="")
                print("|")
                MaxElem+=1               
    print("\n*NOTE: Max results set to 50 ")
#funcion que imprime estadisticas de una carta en especifico
def PrintCardStats(filter):
    print("Processing request...")
    time.sleep(2)
    Select=input(f"\nEnter the {filter} of the card to filter: ('quit' to exit) ")
    if Select.lower() == "quit":
        pass
    else:
        try:
            getResponse = requests.get(f'https://db.ygoprodeck.com/api/v7/cardinfo.php?{filter}={Select}')
            if getResponse.status_code == 200:
                data= getResponse.json()
            for elem in data["data"]:    
                print("\nID: ",elem["id"],"\nName: ",elem["name"],"\nType: ",elem["type"],
                    "\nAttack: ",elem["atk"],"\nDefense: ",elem["def"],"\nLevel: ",elem["level"],"\nRace: ",elem["race"],"\nAttribute: ",elem["attribute"])
            
            Next()
        except:
            print("-Incorrect Value or card does not exists") 
            print(" Returning  to main menu\n") 
            time.sleep(2) 

def Next():
    global cont
    select=input("\nReturn to menu? (Y/N): ")
    time.sleep(1) 
    if select.upper() == "Y":
        pass
    elif select.upper() == "N":
        cont=False
    else:
        print("\n-Invalid choice. Returning  to main menu\n") 
        time.sleep(1) 



def Menu(): 
    global cont
    while cont:    
        print(" ________________________"'\n'
            "|  Welcome to Yu-Gi-Oh!: |"'\n'
            "|        Data Base       |"'\n'
            "|                        |"'\n'
            "| (1) Get Categories     |"'\n'
            "| (2) Filter Data        |"'\n'        
            "| (3) Exit               |"'\n'
            "|________________________|"'\n')     
        
        select=input("Select an option: ")
        if select == "1":
            print(" _______________________"'\n'
                "|      CATEGORIES:      |"'\n'  
                "|                       |"'\n'
                "| (1) Get Types         |"'\n'
                "| (2) Get Races         |"'\n'        
                "| (3) Get Attributes    |"'\n'
                "| (4) Return            |"'\n'
                "|_______________________|"'\n')
            select=input("Select an option: ")
            if select =="1":
                Gettype() 
                Next()           
            elif select =="2":
                Getrace()
                Next()
            elif select =="3":
                GetAttribute()
                Next()
            elif select == "4":
                Menu()  
            else:        
                print("\n-Invalid choice. Returning  to main menu\n") 
                time.sleep(1)    
        elif select == "2":
            print(" _______________________"'\n'
                "|      Filter Data:     |"'\n'  
                "|                       |"'\n'
                "| (1) Per Type          |"'\n'
                "| (2) Per Race          |"'\n'        
                "| (3) Per Attribute     |"'\n'
                "| (4) Per Card Name     |"'\n'
                "| (5) Per Card ID       |"'\n'
                "| (6) Return            |"'\n'
                "|_______________________|"'\n')
            select=input("Select an option: ")
            if select =="1":
                Gettype()
                FilterFunc("type")            
            elif select =="2":
                Getrace()
                FilterFunc("race")
            elif select =="3":
                GetAttribute()
                FilterFunc("attribute")
            elif select == "4":
                PrintCardStats("name") 
            elif select == "5":
                PrintCardStats("id") 
            elif select == "6":
                Menu() 
            else:        
                print("\n-Invalid choice. Returning  to main menu\n") 
                time.sleep(1)  
        elif select == "3":
            cont = False
            break  
        else:        
            print("\n-Invalid choice")         

Menu()
print("\nEnd of program.\nThanks for the visit!")