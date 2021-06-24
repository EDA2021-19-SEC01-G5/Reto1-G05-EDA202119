"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.DataStructures.arraylist import addLast, getElement
import config as cf
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import shellsort
from DISClib.Algorithms.Sorting import insertionsort 
from DISClib.Algorithms.Sorting import selectionsort
from DISClib.Algorithms.Sorting import mergesort, quicksort
assert cf
import time

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

# Funciones para agregar informacion al catalogo
def newCatalog(tipo_lista):
    """
    Crea el catalogo con la información de videos y de categorias
    """
    if int(tipo_lista) == 0:
        ED = "ARRAY_LIST"
    elif int(tipo_lista) == 1:
        ED = "SINGLE_LINKED"
    else:
        return None
    catalog = {"videos":None, "categorias":None}
    catalog["videos"] = lt.newList(ED)
    catalog["categorias"] = lt.newList(ED)
    return catalog


def addVideo(catalog, video):
    """
    Adiciona la información de un video al catalogo
    """
    lt.addLast(catalog["videos"],video)

def addCategoria(catalog, categoria):
    """
    adiciona a informacion de una categoria
    """
    lt.addLast(catalog["categorias"], categoria)


# Funciones para creacion de datos

#Requerimiento 1

def videosPorcategoriaPais(catalog, categoryId, pais):
    cantidad_videos = lt.size(catalog)
    nueva_lista = lt.newList("ARRAY_LIST")
    for i in range(1,cantidad_videos+1):
        elemento = lt.getElement(catalog,i)
        if elemento["category_id"]==categoryId and elemento["country"]==pais:
            lt.addLast(nueva_lista, elemento)
    return nueva_lista

def comparacionLikes(elemento1, elemento2):
    if int(elemento1["likes"]) < int(elemento2["likes"]):
        return True
    else:
        return False

def requerimiento1(catalog, category_name, country, n, tipo_organizacion, prueba, size):
    opciones = {"0": selectionsort.sort, "1": insertionsort.sort, "2": shellsort.sort, "3": quicksort.sort, "4": mergesort.sort}
    categorias = catalog["categorias"]
    cantidad_categorias = lt.size(categorias)
    for i in range(1,cantidad_categorias+1):
        dato = lt.getElement(categorias,i)
        if dato["name"].lower() == category_name.lower():
            category_id = dato["id"]
    if prueba == False:
        nueva_lista = videosPorcategoriaPais(catalog["videos"],category_id,country)
    else:
        nueva_lista = lt.subList(catalog['videos'], 0, size)
    # organizacion
    t_start = time.time_ns()
    organizada = opciones[tipo_organizacion](nueva_lista, comparacionLikes)
    t_end = time.time_ns()

    if prueba:
        organizada = videosPorcategoriaPais(organizada,category_id,country)

    t_total = t_end - t_start
    lista_final = lt.newList("ARRAY_LIST")
    for j in range(lt.size(organizada), lt.size(organizada)-n , -1):
        if j <= lt.size(organizada) and j> 0:
            lt.addLast(lista_final,lt.getElement(organizada,j))
        else:
            pass
    return lista_final, t_total


# requerimiento 2



def diasTrending(elemento):
    trending_date = elemento["trending_date"]
    publicacion = elemento["publish_time"]
    año_trending = int(trending_date[0:2])
    dia_trending = int(trending_date[3:5])
    mes_trending = int(trending_date[6:8])
    año_publicacion = int(publicacion[2:4])
    mes_publicacion = int(publicacion[5:7])
    dia_publicacion = int(publicacion[8:10])
    total_dias  = dia_trending-dia_publicacion
    total_dias += (mes_trending-mes_publicacion)*30
    total_dias += (año_trending-año_publicacion)*12*30
    return total_dias

def obtenerRatio(elemento):
    likes = int(elemento["likes"])
    dislikes = int(elemento["dislikes"])
    if dislikes > 0:
        ratio = likes/dislikes
    else:
        ratio = likes
    return ratio

def comparacionDiasRatioPais(elemento1, elemento2):
    dias1 = diasTrending(elemento1)
    dias2 = diasTrending(elemento2)
    ratio1 = obtenerRatio(elemento1)
    ratio2 = obtenerRatio(elemento2)
    if ratio1 > 10 and ratio2 <= 10:
        return True
    elif ratio1 <= 10 and ratio2 > 10:
        return False
    else:
        if dias1 > dias2:
            return True
        else:
            return False

def requerimiento2(catalog, country):
    nueva_lista = mergesort.sort(catalog["videos"], comparacionDiasRatioPais)
    longitud = lt.size(nueva_lista)
    for i in range(1,longitud+1):
        elemento = lt.getElement(nueva_lista, i)
        if elemento["country"].lower() == country.lower():
            ratio = str(obtenerRatio(elemento))
            dias = str(diasTrending(elemento))
            datos = lt.newList("ARRAY_LIST")
            lt.addLast(datos, elemento["title"])
            lt.addLast(datos, elemento["channel_title"])
            lt.addLast(datos, elemento["country"])
            lt.addLast(datos, ratio)
            lt.addLast(datos, dias)
            return datos


# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento