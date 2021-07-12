﻿
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
import gc
from tabulate import tabulate
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf

default_limit = 1000
sys.setrecursionlimit(default_limit*400000)
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
    print("3- Obtener el video que mas dias ha sido trending en un pais especifico, cuyo ratio_likes_dislikes es altamente positivo.")
    print("4- Obtener el video que más dias ha sido trending para una categoría específica cuya percepción es sumamente positiva. ")
    print("5- Conocer los n videos diferentes con mas comentarios en un pais con un tag especifico.")


def initCatalog(tipo_lista):
    return controller.initcatalog(tipo_lista)


def loadData(catalog):
    controller.loadData(catalog)


def printCategorias(catalog):
    print("Información sobre las categorias: \n")
    cantidad_categorias = lt.size(catalog["categorias"])
    for i in range(1, cantidad_categorias+1):
        print(lt.getElement(catalog["categorias"], i))


def printPrimervideo(catalog):
    elemento = lt.firstElement(catalog["videos"])
    print("\n Datos del primer video cargado: \n")
    print("Titulo : ", elemento["title"])
    print("Nombre del canal : ", elemento["channel_title"])
    print("Fecha de trending : ", elemento["trending_date"])
    print("Pais : ", elemento["country"])
    print("Likes : ", elemento["likes"])
    print("Dislikes : ", elemento["dislikes"], "\n")
    print(elemento.keys())


def requerimiento1(catalog, category_name, country, n, tipo_organizacion):
    lista = controller.requerimiento1(
        catalog, category_name, country, n, tipo_organizacion)
    longitud = lt.size(lista[0])
    if longitud < n:
        print("La cantidad de videos pedidos excede la cantidad posible. \n A continuación de muestran dos los libros de la categoria deseada y el pais deseado, organizados según la cantidad de likes")
    header = ["", "trending date", "titulo", "nombre del canal",
              "fecha publicacion", "vistas", "likes", "dislikes"]
    mostrar = []
    for i in range(1, longitud+1):
        elemento = lt.getElement(lista[0], i)
        mostrar.append([i, elemento["trending_date"], elemento["title"], elemento["channel_title"],
                       elemento["publish_time"], elemento["views"], elemento["likes"], elemento["dislikes"]])
    print(tabulate(mostrar, headers=header))
    print("Tiempo [ms]: ", f"{lista[1]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{lista[2]:.3f}")

def requerimiento2(catalog, country):
    datos = controller.requerimiento2(catalog, country)
    header = ["\nTitulo: ", "Nombre del canal: ",
              "Pais: ", "ratio_likes_dislikes: ", "Dias: "]
    longitud = lt.size(datos[0])
    if longitud != 5:
        print("No se entro un nombre de pais valido o dentro de los datos")
    else:
        for i in range(1, longitud+1):
            print(header[i-1], lt.getElement(datos[0], i))
    print("\n")
    print("Tiempo [ms]: ", f"{datos[1]:.3f}", "  ||  ",
            "Memoria [kB]: ", f"{datos[2]:.3f}")


def requerimiento3(catalog, category_name):
    header = ["\nTitulo: ", "Nombre del canal: ",
              "ID de Categoria: ", "ratio_likes_dislikes: ", "Dias: "]
    print("Encontrando los archivos ... \n")
    data = controller.requerimiento3(catalog, category_name)
    if len(data[0]) != 5:
        print("No se encontraron datos para la categoria ingresada")
    else:
        for i in range(len(data[0])):
            print(header[i], data[0][i])
    print("\n")
    print("\n")
    print("Tiempo [ms]: ", f"{data[1]:.3f}", "  ||  ",
            "Memoria [kB]: ", f"{data[2]:.3f}")



def requerimiento4(catalog, country, tag, n):
    print("Encontrando los archivos ... \n")
    lista = controller.requerimiento4(catalog, country, tag, n)
    longitud_lista = lt.size(lista[0])
    if n != longitud_lista:
        print("No fue posible encontrar la cantidad de datos pedidos. \nSe entregan la cantidad maxima posible. \n")
    header = ["title", "channel_title", "publish_time",
              "views", "likes", "dislikes", "comment_count", "tags"]
    datos = []
    for i in range(1, longitud_lista+1):
        datos.append([])
        video = lt.getElement(lista[0], i)
        for j in range(len(header)):
            datos[i-1].append(video[header[j]])
    print(tabulate(datos, headers=header))
    print("\n")
    print("Tiempo [ms]: ", f"{lista[1]:.3f}", "  ||  ",
            "Memoria [kB]: ", f"{lista[2]:.3f}")



"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        tipo_lista = input(
            "Ingrese el tipo de lista con el que desea cargar la infromación. \n0 para ARRAY_LIST o 1 para SINGLE_LINKED: ")
        print("Cargando información de los archivos ....")
        catalog = initCatalog(tipo_lista)
        if catalog:
            loadData(catalog)
            print("información cargada \n")
            print("Total de registros de videos cargados : ",
                  lt.size(catalog["videos"]), "\n")
            printCategorias(catalog)
            printPrimervideo(catalog)
        else:
            print(
                "\nNo ingreso una opcion de tipo de dato valida, por favor intente de nuevo.\n")

    elif int(inputs[0]) == 2:
        category_name = input(
            "Ingrese la categoria de la cual desea obtener información: ")
        country = input(
            "Ingrese el pais del cual desea obtener información: ")
        n = int(input("Ingrese la cantidad de elementos que quiere ver: "))
        tipo_organizacion = "4"
        requerimiento1(catalog, category_name,
                           country, n, tipo_organizacion)

    elif int(inputs[0]) == 3:
        country = input(
            "Ingrese el pais del cual quiere obtener la información: ")
        requerimiento2(catalog, country)

    elif int(inputs[0]) == 4:
        category_name = input(
            "Ingrese la categoría de la cual quiere obtener la información: "
        )
        requerimiento3(catalog, category_name)

    elif int(inputs[0]) == 5:
        country = input(
            "Ingrese el pais del cual quiere obtener la información: ")
        tag = input("Ingrese el tag del cual quiere obtener la información: ")
        n = int(input("Ingrese la cantidad de elemento que desea obtener: "))
        requerimiento4(catalog, country, tag, n)
    else:
        sys.exit(0)
sys.exit(0)
