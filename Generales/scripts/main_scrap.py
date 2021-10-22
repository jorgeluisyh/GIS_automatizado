#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


ruta_output = "output"
dirgenerales = os.path.dirname(os.path.dirname(__file__))
scriptsdir = os.path.join(dirgenerales, 'scripts')
sourcesdir = os.path.join(dirgenerales, 'sources')
## Desarrollo
imgsdir_output = os.path.join(sourcesdir, 'elBromercio/images')
## Produccion
# imgsdir_output = os.path.join(ruta_output, 'images')


dict_noticias= dict()


def get_premium_news():
	"""
	Obtiene todas las urls de las noticias con categoria de suscriptor digital de la pagina de El Comercio
	estas url son almacenadas en el diccionario dict_noticias
	"""
	global dict_noticias

	diario = "https://elcomercio.pe"
	res = requests.get(diario)
	contenido = res.content
	sopa = BeautifulSoup(contenido,'html.parser')
	tag = 'a'
	clase = 'featured-story__title-link title-xs line-h-sm overflow-hidden'

	mydivs = sopa.find_all(tag, {"class": clase})

	for num, div in enumerate(mydivs, 1):
		dict_noticias[num]= [diario+div["href"]]
		dict_noticias[num].append(div.get_text().encode('utf-8'))



def getSubjectandImage(url_noticia):
	"""
	Obtenemos la categoría de la notica : Economía, Política, Sociales, etc
	Obtenemos también la url de la imagen principal de la noticia
	"""
	tag = 'img'
	clase = "s-multimedia__image w-full o-cover s-multimedia__image--big"
	res = requests.get(url_noticia)
	contenido = res.content
	sopa = BeautifulSoup(contenido,'html.parser')
	# print sopa.prettify('utf-8')
	imgdiv = sopa.find_all(tag,{"class": clase})[0]
	imgurl = imgdiv["src"]
	titulo = sopa.find('title').get_text().encode('utf-8')
	keyword = titulo.split('|')[-2]
	tema =  keyword.strip()
	return tema,imgurl


def getcontenido(url_noticia):
	"""
	Obtenemos el texto principal de la notica(en proceso de mejora de scrap)
	"""
	res = requests.get(url_noticia)
	contenido = res.content
	sopa = BeautifulSoup(contenido,'html.parser')
	titulo = sopa.find('title').get_text()
	print(titulo.encode('utf-8'))

	grupos_texto=sopa.find_all(['h2','p'])
	parrafos = [x.get_text().encode('utf-8')for x in grupos_texto]
	datos = u'\n'.join(parrafos)
	return datos


def downloadfile(name,url,path,type):
	'''
	:param name: nombre que tendra el archivo al ser descargado
	:param url: enlace de descarga
	:param path: ruta donde se almacenara el archivo
	:param type: formato del archivo de salida
	:return:
	'''
	name=name+".%s"%type
	r=requests.get(url)
	print("****Connected****")
	outpath = os.path.join(path,name)
	f=open(outpath,'wb');
	print("Downloading.....%s"%name)
	for chunk in r.iter_content(chunk_size=255):
		if chunk: # filter out keep-alive new chunks
			f.write(chunk)
	print("Done")
	f.close()


def reemplazardatosenhtml():
	"""
	Reemplazae datos del diccionario en el index.html y las subpaginas

	dict_noticias {1:[url_noticia, titulo, tema, imgurl, resumen, contenido]}
	"""
	html_ini = os.path.join(sourcesdir,'elBromercio/index.html')
	# ruta salida desarrollo
	# html_fin = os.path.join(sourcesdir,'elBromercio/index_copy.html')
	# ruta salida produccion
	html_fin = os.path.join(ruta_output,'index.html')

	html = open(html_ini) 
	sopa_index = BeautifulSoup(html, 'html.parser')

	for num in range(1,4):
		tag_titulo = sopa_index.find('a',{"id":"titulo_%d"%num})
		tag_titulo.string = dict_noticias[num][1]

		tag_tema = sopa_index.find('a',{"id":"tema_%d"%num})
		tag_tema.string = dict_noticias[num][2]
		
		tag_resumen = sopa_index.find('p',{"id": "resumen_%d"%num})
		tag_resumen.string = dict_noticias[num][4]

		reemplazardatosenpage(num)
	
	with open(html_fin, "wb") as f_output:
		f_output.write(sopa_index.prettify("utf-8"))

def reemplazardatosenpage(num):
	"""
	Reemplazar los datos de la noticia principal dentro de la subpagina
	"""
	html_ini = os.path.join(sourcesdir,'elBromercio/pages/single%d.html'%num)
	# ruta output desarrollo
	# html_fin = os.path.join(sourcesdir,'elBromercio/pages/single%d_copy.html'%num)
	# ruta output produccion
	html_fin = os.path.join(ruta_output,'pages/single%d.html'%num)
	
	html = open(html_ini) 
	sopa_single = BeautifulSoup(html, 'html.parser')

	tag_tema = sopa_single.find('a',{"class":"stuff_category"})
	tag_tema.string = dict_noticias[num][2]

	tag_titulo = sopa_single.find('a',{"id":"titulo"})
	tag_titulo.string = dict_noticias[num][1]

	tag_noticia = sopa_single.find('p',{"id":"noticia"})
	tag_noticia.string = dict_noticias[num][5]


	with open(html_fin, "wb") as f_output:
		f_output.write(sopa_single.prettify("utf-8"))

	




def main():
	get_premium_news()
	for i in range(1,4):

		url = dict_noticias[i][0]
		tema, img_url = getSubjectandImage(url)
  		nameimg = "img_%d"%i
		downloadfile(nameimg, img_url, imgsdir_output,'jpg')

		texto_noticia = getcontenido(url)
		resumen = texto_noticia[0:248]+"..."
		dict_noticias[i].append(tema)
		dict_noticias[i].append(img_url)
		dict_noticias[i].append(resumen)
		dict_noticias[i].append(texto_noticia)

	

if __name__ == '__main__':
	main()
	reemplazardatosenhtml()
