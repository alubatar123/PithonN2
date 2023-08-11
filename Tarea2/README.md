# Tarea 1 Esteban Garro

## Introduccion

 La API escogida proviene de https://ygoprodeck.com/api-guide/ la cual proporciona una base
 de datos de diferentes estadisticas de cada carta de Yu-Gi-Oh asi como sus caracteristicas.
  Los metodos creados permiten filtrar por algunas de las subcategorias asi como ver
 estadisticas por carta.
  Actualmente existen 12,456 cartas, por lo que se limitó la cantidad de valores a imprimir. 

## Consumo de datos

 Basados en las funciones de la Tarea 1, las nuevas funciones permiten resumir y graficar los datos 
 filtrados por Raza, Tipo o Atributo.

### FilterData

Función para convierte los datos del API a un dataframe con solo las columnas relevantes

### PrintStats

Función que imprime los datos mas relevantes de la categoria seleccionada. Tales como:

* Carta con Nivel Maximo
* Carta con Ataque Maximo
* Carta con Defensa Maximo
* 6 primeras cartas con Nivel Maximo
* 6 primeras cartas con Ataque Maximo
* 6 primeras cartas con Defensa Maximo

### PrintGraph Level():

Funcion que muestra cuantas cartas hay por nivel por categoria    

### PrintGraph AtkDef():

Funcion que compara Def y Atk de las 15 cartas con mayor Nivel

### PrintGraph CardStats():

Grafico de radar que permite saber que tal son los valores de la carta con max Nivel de dicha categoria en comparacion a los valores Maximos existentes de Nivel, Ataque y Defensa. No se toman en cuenta cartas especiales

### Next()
Función permite salir o regresar el menu principal

### Menu()
Función que muestra un menu principal con las diferentes Funciónes disponibles