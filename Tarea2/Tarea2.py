import Tarea1 as T1
import requests
import pandas as pd
import time
import matplotlib.pyplot as plt

cont=True
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
            return MyDicct,filter

        except:
            print("-Incorrect Value or filter does not exists")
            print(" Returning  to main menu\n") 
            time.sleep(2) 

def PrintStats(Filter):    
    data=pd.DataFrame.from_dict(FilterData(Filter))
    print(data)
    print("Processing request...")
    time.sleep(2)
    MaxLevel = data.loc[data["Level"].idxmax(), "Level"]
    MaxDef = data.loc[data["Def"].idxmax(), "Def"]
    MaxAttk= data.loc[data["Atk"].idxmax(), "Atk"]
    TopLevel=data.nlargest(10,'Level')
    TopDef=data.nlargest(3,'Def')
    TopAtk=data.nlargest(3,'Atk')
    Mode=data['Level'].mode()[0]#Ya que retorna un objecto, agregamos [0] para extraer el valor.
    print("\nSUMMARY\n")
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
    def Level():
        #Funcion que muestra cuantas cartas hay por nivel por categoria        
        groupLevel = data.groupby("Level").count()
        plt.bar(groupLevel.index, groupLevel["Name"])
        plt.xlabel("LEVEL")
        plt.ylabel("COUNT")
        plt.title(f"Level per {FilterName}",weight='bold', fontsize=18)    
        plt.show()

    def AtkDef():

        Sdata=data.sort_values("Atk", ascending=False)
        newDF=Sdata[["Name","Atk","Def"]].copy().head(15)
        
        ax = newDF.plot.bar(x=('Name'), width=1)        
        ax.set_xlabel('CARD NAME')
        ax.set_ylabel('Stats')
    #https://datavizpyr.com/how-to-annotate-bars-in-grouped-barplot-in-python/
        #plt.xlabel("Continent", size=16)
        #plt.ylabel("LifeExp", size=16)
        for container in ax.containers:            
            ax.bar_label(container,rotation=90,size=13,label_type='center')
        ax.set_title(f"Top Stats per {FilterName}",weight='bold', fontsize=15)    
        
        #plt.title
        plt.show()
    AtkDef()    

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

#Menu() 
print("\nEnd of program.\nThanks for the visit!")               
T1.Gettype()
PrintGraph("type")