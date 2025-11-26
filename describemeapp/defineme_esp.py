import networkx as nx
import os
import codecs
import nltk
import string
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
from operator import itemgetter
import xlrd
import spacy

nlp = spacy.load('es_core_news_sm')

def calcula_total_concepto(fila,hoja):
	suma = 0
	while((fila+1) < hoja.nrows and hoja.cell(fila+1,0).value != "======"):
		if hoja.cell(fila,2).value!= '':
			suma += float(hoja.cell(fila,2).value)
		fila += 1
	return suma

def ConstruyeGrafos():
	lista_grafos = []
	fname = 'corpus/original.xls'
	xl_workbook = xlrd.open_workbook(fname)
	xl_sheet = xl_workbook.sheet_by_index(7)
	libro = xlrd.open_workbook(fname)
	hoja = libro.sheet_by_index(7)
	GrafoFreq=nx.Graph()
	GrafoTiempo=nx.Graph()
	GrafoAso= nx.Graph()
	num_cols = xl_sheet.ncols 
	estimulo = ''
	lemma = ''
	frecuencia = 0
	tiempo = 0
	asociacion = 0
	i=0
	nodos={}
	total = 0
	for row_idx in range(0, xl_sheet.nrows-1):
		cell_obj = xl_sheet.cell(row_idx,0)
		cadena = cell_obj.value
		if cadena == '--PALABRAS--':		
			total_por_concepto = calcula_total_concepto(row_idx+1,hoja)						
			continue
		elif cadena == '======': 
			estimulo = xl_sheet.cell(row_idx+1, 0).value		
		elif cadena == '' or cadena == '*':
			continue
		elif xl_sheet.cell(row_idx,2).value == '':
			continue
		else:
			frecuencia = xl_sheet.cell(row_idx, 2).value
			tiempo = xl_sheet.cell(row_idx, 3).value
			asociacion = xl_sheet.cell(row_idx, 5).value
			lemma = xl_sheet.cell(row_idx, 1).value
			estimulo = estimulo.strip()
			lemma = str(lemma)
			lemma = lemma.strip()
			if estimulo=="colores" or lemma=="colores":
				print("Se encontró en la línea ",row_idx)
			GrafoFreq.add_edge(estimulo,lemma,weight=total_por_concepto-int(frecuencia))
			GrafoTiempo.add_edge(estimulo,lemma,weight=float(tiempo))
			GrafoAso.add_edge(estimulo,lemma,weight=float(asociacion))
	lista_grafos.append(GrafoFreq)
	lista_grafos.append(GrafoTiempo)
	lista_grafos.append(GrafoAso)	
	return lista_grafos

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

def limpia_lematiza(cadena):
    palabras_funcionales=nltk.corpus.stopwords.words("spanish")
    limpiado = ""
    for c in string.punctuation:
        cadena = cadena.replace(c,"")
    for palabra in cadena.split(" "):
        if palabra not in palabras_funcionales: 
            doc = nlp(palabra)
            limpiado = limpiado + doc[0].lemma_ + " "
    return limpiado  

'''def diccionario_nap(definicion):
    grafos = ConstruyeGrafos()
    grafo_frec = grafos[0]	
    grafo_tiempo = grafos[1]	
    grafo_asoc = grafos[2]
    texto = limpia_lematiza(definicion)
    texto = texto.lower()
    tokens = texto.split(" ")
    subconjunto_lemas = []
    for palabra in tokens:
        if palabra in grafo_asoc.nodes():
            subconjunto_lemas.append(palabra)
    if len(subconjunto_lemas) > 0:
        btwnCent_subset_asociacion = nx.betweenness_centrality_subset(grafo_asoc, subconjunto_lemas,subconjunto_lemas, normalized=True,weight='weight')		
        encontrados = sorted(btwnCent_subset_asociacion.items(),key=itemgetter(1), reverse=True)[0:100]
        return conceptos(encontrados,subconjunto_lemas)
    else:
        return "Descripción muy corta, favor de ampliar su descripción."'''

def lista_conceptos(lista,subconjunto):
    datos = ""
    if len(lista) <= 100:
        tope = len(lista)
    else:
        tope = 100
    for x in range(0,tope):
        if str(lista[x][0]) not in subconjunto:
            datos = datos + ',' + str(lista[x][0]).strip()
    return datos

def diccionario_nap(definicion, grafo_asoc):
    texto = limpia_lematiza(definicion)
    texto = texto.lower()
    tokens = texto.split(" ")
    subconjunto_lemas = []
    encontrados_final = []
    for palabra in tokens:
        if palabra in grafo_asoc.nodes():
            subconjunto_lemas.append(palabra)
    if len(subconjunto_lemas) > 0:
        btwnCent_subset_asociacion = nx.betweenness_centrality_subset(grafo_asoc, subconjunto_lemas,subconjunto_lemas, normalized=True,weight='weight')		
        encontrados = sorted(btwnCent_subset_asociacion.items(),key=itemgetter(1), reverse=True)[0:20]
        for encontrado in encontrados:
            if encontrado[1] > 0.0:
                encontrados_final.append(encontrado)
            if len(encontrados_final) == 0:
                return "Descripción poco específica."
        return lista_conceptos(encontrados_final,subconjunto_lemas)
    else:
        return "Descripción muy corta favor de ampliar su descripción."

if __name__ == "__main__":
  print('comenzando!')
  grafos = ConstruyeGrafos()
  grafo_esp = grafos[2]
  print(diccionario_nap("Transporte terrestre público de pasajeros muy grande", grafo_esp))
  print(diccionario_nap("Alimento elaborado con leche. existen diferentes tipos: manchego, cotija. panela entre otros.", grafo_esp))
