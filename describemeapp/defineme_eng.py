import networkx as nx
import os
import codecs
import nltk
import string
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
from operator import itemgetter



def florida_graph():
    G_asoc= nx.Graph()
    ruta = "corpus/separados_florida/"
    directorio = os.listdir(ruta)
    for archivo in directorio:
        file = open(ruta+"/"+archivo,encoding="utf-8")       
        G_asoc.add_node(archivo)
        lineas = file.readlines()
        for linea in lineas:
            linea = linea.strip("\n")
            datos = linea.split(",")
            respuesta = str(datos[0])
            asociacion = float(datos[2])
            G_asoc.add_node(respuesta)
            G_asoc.add_edge(archivo,respuesta,weight=asociacion)
    return G_asoc



'''def conceptos(lista,subconjunto):
    datos = []
    if len(lista) <= 100:
        tope = len(lista)
    else:
        tope = 100
    for x in range(0,tope):
        if str(lista[x][0]) not in subconjunto:
            datos.append(str(lista[x][0]).strip())
    return datos'''



def construye_sugrafo_vecinal(nivel, grafo_asoc, subconjunto):
    nuevo_grafo_a = nx.Graph()
    vecinos = set()
    for lema in subconjunto:
        vecinos.add(lema)
    for i in range (nivel):
        nuevo_conjunto = set()
        for vecino in vecinos:
            for nodo in nx.all_neighbors(grafo_asoc,vecino):
                nuevo_conjunto.add(nodo)
        vecinos = vecinos.union(nuevo_conjunto)       
    nuevo_grafo_a = nx.Graph(grafo_asoc.subgraph(vecinos))
    return nuevo_grafo_a



def limpia_lematiza(cadena):
    palabras_funcionales=nltk.corpus.stopwords.words("english")
    limpiado = ""
    for c in string.punctuation:
        cadena = cadena.replace(c,"")
    for palabra in cadena.split(" "):
        if palabra not in palabras_funcionales: 
            limpiado = limpiado + wordnet_lemmatizer.lemmatize(palabra) + " "
    return limpiado



'''def diccionario(definicion):
    grafo_asoc = florida_graph()
    texto = limpia_lematiza(definicion)
    tokens = texto.split(" ")
    subconjunto_lemas = []
    for palabra in tokens:
        if palabra in grafo_asoc.nodes():
            subconjunto_lemas.append(palabra)
    if len(subconjunto_lemas)>0:
        ga = construye_sugrafo_vecinal(1,grafo_asoc,subconjunto_lemas)
        if ga.number_of_nodes()>0:
            btwnCent_subset_asociacion = nx.betweenness_centrality_subset(ga, subconjunto_lemas,subconjunto_lemas, normalized=True,weight='weight')
            encontrados = sorted(btwnCent_subset_asociacion.items(),key=itemgetter(1), reverse=True)[0:100]
    return conceptos(encontrados,subconjunto_lemas)'''



def lista_conceptos(lista,subconjunto):
    datos = ""
    if len(lista) <= 100:
        tope = len(lista)
    else:
        tope = 100
    for x in range(0,tope):
        if str(lista[x][0]) not in subconjunto:
            datos = datos + ',' + str(lista[x][0]).strip()
            #datos.append(str(lista[x][0]).strip())
    return datos



def diccionario_limitado_eng(definicion, grafo_asoc):
    texto = limpia_lematiza(definicion)
    tokens = texto.split(" ")
    subconjunto_lemas = []
    for palabra in tokens:
        if palabra in grafo_asoc.nodes():
            subconjunto_lemas.append(palabra)
    if len(subconjunto_lemas)>0:
        ga = construye_sugrafo_vecinal(1,grafo_asoc,subconjunto_lemas)
        if ga.number_of_nodes()>0:
            btwnCent_subset_asociacion = nx.betweenness_centrality_subset(ga, subconjunto_lemas,subconjunto_lemas, normalized=True,weight='weight')
            encontrados = sorted(btwnCent_subset_asociacion.items(),key=itemgetter(1), reverse=True)[0:20]
    return lista_conceptos(encontrados,subconjunto_lemas)

#print(diccionario("ancient fishes"))