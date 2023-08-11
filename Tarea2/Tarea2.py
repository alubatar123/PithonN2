import Tarea1 as T1
import requests
import pandas as pd
import time
import matplotlib.pyplot as plt

cont=True
#Funcion que crea un dataframe dependiendo la categoria escogida
def FilterData(filter):
    Select=input(f"\nEnter the name of the {filter} to filter: ('quit' to return) ")
    if Select.lower() == "quit":
        pass 
    else:
        try:   
            getResponse = requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?{filter}={Select}")  
            if getResponse.status_code == 200:
                data= getResponse.json()   
                MyDicct={"Name":[],"Type":[],"Level":[],"Def":[],"Atk":[],"Race":[],"Attribute":[]}           
            for elem in data["data"]:    
                try:
                    #se filtran solo columnas validas. Cartas sin Level son de coleccion solamente
                    if elem['level']!=None: 
                        MyDicct["Name"].append(elem["name"])
                        MyDicct["Type"].append(elem["type"])
                        MyDicct["Level"].append(elem["level"])
                        MyDicct["Def"].append(elem["def"])
                        MyDicct["Atk"].append(elem["atk"])
                        MyDicct["Race"].append(elem["race"])
                        MyDicct["Attribute"].append(elem["attribute"])
                except KeyError:
                    pass  
            return MyDicct,Select

        except:
            print("-Incorrect Value or filter does not exists")
            print(" Returning  to main menu\n") 
            time.sleep(2) 

#funcion que imprime ciertos valores resumidos dependiendo la categoria escogida
def PrintStats(Filter):    
    TempDicct,FilterName=(FilterData(Filter))
    data=pd.DataFrame.from_dict(TempDicct)
    print("Processing request...")
    time.sleep(2)
    MaxLevel = data.loc[data["Level"].idxmax(), "Level"]#Carta de mayor nivel
    MaxDef = data.loc[data["Def"].idxmax(), "Def"] #Carta con mayor defense
    MaxAttk= data.loc[data["Atk"].idxmax(), "Atk"]#Carta con mayor ataque
    TopLevel=data.nlargest(6,'Level') #6primeras cartas con max nivel
    TopDef=data.nlargest(6,'Def')#6 primeras cartas con max def
    TopAtk=data.nlargest(6,'Atk')#6 primeras cartas con max atk
    Mode=data['Level'].mode()[0]#Ya que retorna un objecto, agregamos [0] para extraer el valor.
    print(f"\nSUMMARY FOR {FilterName}\n")
    print(" • The highest level is:",MaxLevel)
    print("\n • The highest defense is:",MaxDef)
    print("\n • The highest attack is:",MaxAttk)
    print("\n • The most common level is:",Mode)
    print("\n • The top level cards are:\n",TopLevel)
    print("\n • The top defense cards are:\n",TopDef)
    print("\n • The top attack cards are:\n",TopAtk)
    Next()

def PrintGraph(Filter):
    TempDicct,FilterName=(FilterData(Filter))
    data=pd.DataFrame.from_dict(TempDicct)
    #Se define parametros visuales
    font = {'family': 'serif', 'color':  'navy','size': 16,'weight': 'bold',}
    Tfont= {'family': 'sans-serif', 'color':  'teal','weight': 'bold','size': 18,}

    def Level():
        #Funcion que muestra cuantas cartas hay por nivel por categoria        
        groupLevel = data.groupby("Level").count()
        plt.bar(groupLevel.index, groupLevel["Name"])
        plt.xlabel("LEVEL", fontdict=font)
        plt.ylabel("TOTAL CARDS", fontdict=font)
        plt.title(f"Sum of all Level cards matching '{FilterName}'",fontdict=Tfont)    
        plt.show()

    def AtkDef():
        #Funcion que compara Def y Atk de las 15 cartas con mayor Nivel
        Sdata=data.sort_values("Level", ascending=False)
        newDF=Sdata[["Name","Atk","Def"]].copy().head(15)        
        ax = newDF.plot.bar(x=('Name'), width=0.9) 
        #ax.set_ylabel("Stats",  fontdict=font)
        for container in ax.containers:            
            ax.bar_label(container,rotation=90,size=11,label_type='center')
        ax.set_title(f"Top 15 CARD Stats matching '{FilterName}'",fontdict=Tfont)  
        plt.xlabel("CARD NAME", fontdict=font)
        plt.ylabel("Atk/Def Points", fontdict=font)       
        plt.tight_layout(pad=0.2)
        
        plt.show()

    def CardStats():
        #Grafico de radar que permite saber que tal son los valores de la carta con max Nivel
        df = pd.DataFrame({
            'Name': [data.loc[data["Level"].idxmax(), "Name"]],
            'Level(max 12)': [(data.loc[data["Level"].idxmax(), "Level"]/12*5000)],
            'Atk(max 5000)': [data.loc[data["Level"].idxmax(), "Atk"]],
            'Def(max 5000)': [data.loc[data["Level"].idxmax(), "Def"]]})

        values=df.loc[0].drop('Name').values.flatten().tolist()
        values += values[:1]
        angles = [n / float(len(list(df)[1:])) * 2 * 3.14 for n in range(len(list(df)[1:]))]
        angles += angles[:1]
        ax = plt.subplot(111, polar=True)
        plt.xticks(angles[:-1], (list(df)[1:]), color='navy', size=10)
        plt.yticks([1000,2000,3000,4000,5000], color="white", size=7,visible=False)
        plt.ylim(0,5100)       
        ax.plot(angles, values, linewidth=1, linestyle='solid',color='darkgreen')
        
        ax.fill(angles, values, 'b', alpha=0.1)       
        ax.annotate("ATTACK=" +str(df["Atk(max 5000)"].iloc[0])+"\n"
                    "DEFENSE=" +str(df["Def(max 5000)"].iloc[0])+"\n"
                    "LEVEL=" +str(int((df["Level(max 12)"].iloc[0]/5000)*12))
                    , xy=(-1, 9), xycoords='axes points',
                    size=9, ha='right', va='top',
                    bbox=dict(boxstyle='round', fc='w'))
        Mytitle=df["Name"].iloc[0]
        ax.tick_params(axis='x', which='major', pad=30)
        plt.title(f"STATS FOR CARD WITH HIGHEST LEVEL: '{Mytitle}'\n",fontdict=Tfont)   
        plt.tight_layout(pad=0.2)
        plt.show()
    AtkDef()  
    Level()
    CardStats()
    Next()  

#Funcion que permite salir o seguir en el programa
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
            "|   Database Analytics   |"'\n'
            "|                        |"'\n'
            "| (1) Get Statistics     |"'\n'
            "| (2) Get Graphics       |"'\n'        
            "| (3) Exit               |"'\n'
            "|________________________|"'\n')     
        
        select=input("Select an option: ")
        if select == "1":
            print(" _______________________"'\n'
                "|      Filter by:       |"'\n'  
                "|                       |"'\n'
                "| (1) Type              |"'\n'
                "| (2) Races             |"'\n'        
                "| (3) Attributes        |"'\n'
                "| (4) Return            |"'\n'
                "|_______________________|"'\n')
            select=input("Select an option: ")
            if select =="1":
                T1.Gettype() 
                PrintStats("type")                           
            elif select =="2":
                T1.Getrace()
                PrintStats("race")                
            elif select =="3":
                T1.GetAttribute()
                PrintStats("attribute")                
            elif select == "4":
                Menu()  
        if select == "2":
            print(" _______________________"'\n'
                "|     Get Graph for:    |"'\n'  
                "|                       |"'\n'
                "| (1) Type              |"'\n'
                "| (2) Races             |"'\n'        
                "| (3) Attributes        |"'\n'
                "| (4) Return            |"'\n'
                "|_______________________|"'\n')
            select=input("Select an option: ")
            if select =="1":
                T1.Gettype() 
                PrintGraph("type")                           
            elif select =="2":
                T1.Getrace()
                PrintGraph("race")                
            elif select =="3":
                T1.GetAttribute()
                PrintGraph("attribute")                
            elif select == "4":
                Menu()
        if select == "3":
            cont=False          
Menu() 
print("\nEnd of program.\nThanks for the visit!")               
#T1.Gettype()

#PrintGraph("type")