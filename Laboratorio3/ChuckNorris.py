import requests
cont=True

#Obtiene un Chiste random
def ChisteRandom():
    getResponse = requests.get("https://api.chucknorris.io/jokes/random")    
    if getResponse.status_code == 200:
        data = getResponse.json()        
        print("\nChiste Ramdon:\n  "+data["value"])

#Crea una lista con las categorias del API
def ListarCateg():
    getResponse = requests.get("https://api.chucknorris.io/jokes/categories")    
    if getResponse.status_code == 200:
        categ = getResponse.json()
        return categ

#Muesta las categorias en grupos de 4
def VerCategorias(NumLista):
        Lista=ListarCateg()              
        for Id in range(len(Lista)):
            if Id<4:         
                print(f"• ({Id+NumLista}) {Lista[Id+NumLista-1]}   ",end="")                 
        print("")

#permite escoger una categoria       
def ChisteCategoria():
    Lista=ListarCateg()
    try:
        MiCateg=int(input("\nSeleccione el numero de la categoria deseada: "))
        getResponse = requests.get(f"https://api.chucknorris.io/jokes/random?category={Lista[MiCateg-1]}")    
        if getResponse.status_code == 200:
            chiste = getResponse.json()        
            print(f"\nChiste sobre '{Lista[MiCateg-1]}':\n  "+chiste["value"])
    except IndexError:
        print("Categoria inexistente\n") 
    except ValueError:
        print("Favor digite un numero de la lista\n") 


while cont:    
    print(" _____________________"'\n'
        "|    Bienvenido:      |"'\n'
        "|                     |"'\n'
        "| (1) Chiste Random   |"'\n'
        "| (2) Ver Categorias  |"'\n'
        "| (3) Escoger Chiste  |"'\n'
        "| (4) Salir           |"'\n'
        "|_____________________|"'\n')     
       
    operaracion=input("¿Que operacion desea realizar? ")
    if operaracion == "1":
         print()         
         ChisteRandom()         
    elif operaracion == "2": 
         
         print("\nCategorias disponibles:\n")          
         VerCategorias(1)
         VerCategorias(5)
         VerCategorias(9)
         VerCategorias(13)

    elif operaracion == "3":          
         print("\nCategorias disponibles:\n")          
         VerCategorias(1)
         VerCategorias(5)
         VerCategorias(9)
         VerCategorias(13)
         ChisteCategoria()                  
    elif operaracion == "4":
          cont = False  
    else:        
         print("\nSeleccion invalida\n")      