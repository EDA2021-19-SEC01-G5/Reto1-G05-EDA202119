
"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

#from App.controller import initcatalog
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from tabulate import tabulate

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Conocer los videos con mas likes que son tendencia en un pais en la categoria deseada.")
    print("3- Obtener el video que mas likes ha tenido en un pais especifico, cuyo ratio_likes_dislikes es altamente positivo")



def initCatalog(tipo_lista):
    return controller.initcatalog(tipo_lista)


def loadData(catalog):
    controller.loadData(catalog)


def printCategorias(catalog):
    print("Información sobre las categorias: \n")
    cantidad_categorias = lt.size(catalog["categorias"])
    for i in range(1,cantidad_categorias+1):
        print(lt.getElement(catalog["categorias"],i))
    


def printPrimervideo(catalog):
    elemento = lt.firstElement(catalog["videos"])
    print("\n Datos del primer video cargado: \n")
    print("Titulo : ", elemento["title"])
    print("Nombre del canal : ", elemento["channel_title"])
    print("Fecha de trending : ", elemento["trending_date"])
    print("Pais : ", elemento["country"])
    print("Likes : ", elemento["likes"])
    print("Dislikes : ",elemento["dislikes"], "\n")
    print(elemento.keys())

# requerimiento 1, con division de libros por pais y categoria, para organizar una menor cantidad
# parametro puebaTrue si se quiere hacer la organizacion con todo, false de lo contrario
def requerimiento1(catalog, category_name, country, n, tipo_organizacion, prueba= False, size = 10):
    lista, t_total = controller.requerimiento1(catalog,category_name, country,n, tipo_organizacion, prueba, size)
    longitud = lt.size(lista)
    if longitud < n:
        print("La cantidad de videos pedidos excede la cantidad posible. \n A continuación de muestran dos los libros de la categoria deseada y el pais deseado, organizados según la cantidad de likes")
    header = ["", "trending date", "titulo", "nombre del canal", "fecha publicacion", "vistas", "likes", "dislikes"]
    mostrar = []
    for i in range(1, longitud+1):
        elemento = lt.getElement(lista,i)
        mostrar.append([i, elemento["trending_date"], elemento["title"], elemento["channel_title"], elemento["publish_time"],elemento["views"],elemento["likes"],elemento["dislikes"]])
    print(tabulate(mostrar, headers=header))
    print("\nEl tiempo que le tomo al algoritmo de organización fue de :", t_total, "ns")
    if prueba: 
        return t_total




def requerimiento2(catalog, country):
    datos = controller.requerimiento2(catalog,country)
    header = ["\nTitulo: ", "Nombre del canal: ", "Pais: ", "ratio_likes_dislikes: ", "Dias: "]
    longitud = lt.size(datos)
    if longitud != 5:
        print("No se entro un nombre de pais valido o dentro de los datos")
    else:
        for i in range(1, longitud+1):
            print( header[i-1],lt.getElement(datos,i))
    print("\n")
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        tipo_lista = input("Ingrese el tipo de lista con el que desea cargar la infromación. \n0 para ARRAY_LIST o 1 para SINGLE_LINKED: ")
        print("Cargando información de los archivos ....")
        catalog = initCatalog(tipo_lista)
        if catalog:
            loadData(catalog)
            print("información cargada \n")
            print("Total de registros de videos cargados : ", lt.size(catalog["videos"]),"\n")
            printCategorias(catalog)
            printPrimervideo(catalog)
        else:
            print("\nNo ingreso una opcion de tipo de dato valida, por favor intente de nuevo.\n")

    elif int(inputs[0]) == 2:
        prueba = input("Desea realizar pruebas de funcionamiento? (si/no): ")
        if prueba == "no":
            category_name = input("Ingrese la categoria de la cual desea obtener información: ")
            country = input("Ingrese el pais del cual desea obtener información: ")
            n = int(input("Ingrese la cantidad de elemento que quiere ver: "))
            tipo_organizacion = input("Ingrese el tipo de algoritmo de ordenamiento que desee. \n0 para selection sort, 1 para insertion sort, y 2 para shell sort")
            requerimiento1(catalog,category_name, country, n, tipo_organizacion)
        elif prueba == "si":
            category_name = input("Ingrese la categoria de la cual desea obtener información: ")
            country = input("Ingrese el pais del cual desea obtener información: ")
            n = int(input("Ingrese la cantidad de elemento que quiere ver: "))
            tamaños = [1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000, 256000]
            algoritmos = {"0": "selection sort", "1":"insertion sort" ,"2": "shell sort"}
            tiempos = []
            for a in range(len(algoritmos.keys())): 
                tiempos.append([])
                for i in tamaños:
                    tiempo = requerimiento1(catalog,category_name, country, n, str(a), True,i)
                    tiempos[a].append(tiempo)
            archivo = open("datos_prueba"+str(tipo_lista)+".txt", "w")
            archivo.write("algoritmo, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000, 256000")
            for i in range(3):
                texto = algoritmos[str(i)] + " ,"
                for j in range(len(tiempos[i])):
                    texto = texto + str(tiempos[i][j]) + ", "
                archivo.write(texto)
            archivo.close()
            print(tiempos)

        else:
            print("No seleccionó una opción valida, por favor vuelva a intentar.")

        
    elif int(inputs[0]) == 3:
        country = input("Ingrese el pais del cual quiere obtener la información: ")
        requerimiento2(catalog, country)
    else:
        sys.exit(0)
sys.exit(0)
