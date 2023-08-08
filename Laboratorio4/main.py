import pandas as pd
import matplotlib.pyplot as plt

#se lee el archivo y se pasa a un Dataframe
df = pd.read_csv ('./Laboratorio4/ventas.csv')
print("Data Frame Actual:\n",df)

#Se agrega una nueva columna "Ganancia" del resultado Ventas-Gastos
beneficio=[x for x in (df["Ventas"]-df["Gastos"])]
df["Ganancia"]=beneficio
print("\nData Frame + Beneficio Mensual:\n",df)

#Grafico de Ventas y Gastos a traves de los meses

#cambios visuales del Font
font = {'family': 'serif',
        'color':  'white',
        'weight': 'normal',
        'size': 16,
        }

plt.figure(figsize=(12,5),facecolor='#757EA1')
plt.plot(df["Mes"], df["Ventas"], 'b' ,  label = 'Ventas' ,  linewidth = 2 ) 
plt.plot(df["Mes"], df["Gastos"],  'r' ,  label = 'Gastos' ,  linewidth = 2 ) 
plt.xlabel("Mes".upper(), fontdict=font)
plt.ylabel("Cantidades", fontdict=font)
plt.title("Evolución Ventas y Gastos",weight='bold', fontsize=18)
plt.legend()
plt.show()
