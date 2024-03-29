#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
import time
from bs4 import BeautifulSoup

# USAR EL RELOAD SYS PARA PYTHON27
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")


ruta_output = "output"
dirgenerales = os.path.dirname(os.path.dirname(__file__))
scriptsdir = os.path.join(dirgenerales, 'scripts')
sourcesdir = os.path.join(dirgenerales, 'sources')
## Desarrollo
# imgsdir_output = os.path.join(sourcesdir, 'elBromercio/images')
## Produccion
imgsdir_output = os.path.join(ruta_output, 'images')
logo_bromercio = "https://raw.githubusercontent.com/jorgeluisyh/elBromercio/main/images/logo3.png"


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
		dict_noticias[num].append(div.get_text().encode('utf-8').decode("utf-8") )

def getSoupContent(url_noticia):
	"""
	Obtenemos el contenido de la noticia
	"""
	res = requests.get(url_noticia)
	time.sleep(2)
	contenido = res.content
	sopa = BeautifulSoup(contenido,'html.parser')
	return sopa	


def getSubjectandImage(sopa):
	"""
	Obtenemos la categoría de la notica : Economía, Política, Sociales, etc
	Obtenemos también la url de la imagen principal de la noticia
	"""
	try:
		tag = 'img'
		clase1 = "s-multimedia__image w-full o-cover s-multimedia__image--big"
		clase2 = "s-multimedia__image w-full o-cover"
		# print (sopa.prettify('utf-8'))

		titulo = sopa.find('title').get_text().encode('utf-8').decode("utf-8") 		
		keytag = titulo.split('|')[-2]
		tema =  keytag.strip()

		imgurl = logo_bromercio
		imgdiv = sopa.find_all(tag,{"class": [clase1, clase2]})[0]
		imgurl = imgdiv["src"]
	except:
		print("No se encontro imagen en la url: ")
	
	return tema,imgurl


def getcontenido(sopa):
	"""
	Obtenemos el texto principal de la notica(en proceso de mejora de scrap)
	"""
	# titulo = sopa.find('title').get_text()
	# print(titulo.encode('utf-8').decode("utf-8") )

	# grupos_texto=sopa.find_all(['h2','p'])
	# parrafos = [x.get_text().encode('utf-8').decode("utf-8") for x in grupos_texto]
	# datos = u'\n'.join(parrafos)
	# return datos
	cls_resumen = "sht__summary"
	resumen = sopa.find('h2',{"class": cls_resumen})
	resumen = resumen.get_text() if resumen else "resumen no disponible"


	clase = "story-contents__content story-content__nota-premium paywall no_copy"
	noticia_princ = sopa.find('div',{"class": clase})
	noticia_princ["style"]=""
	objeto_noticia =noticia_princ.contents

	return resumen, objeto_noticia



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
	Reemplazar datos del diccionario en el index.html y las subpaginas

	dict_noticias {1:[url_noticia, titulo, tema, imgurl, resumen, contenido]}
	"""
	html_ini = os.path.join(sourcesdir,'elBromercio/index.html')
	# ruta salida desarrollo
	# html_fin = os.path.join(sourcesdir,'elBromercio/index_copy.html')
	# ruta salida produccion
	html_fin = os.path.join(ruta_output,'index.html')

	html = open(html_ini) 
	sopa_index = BeautifulSoup(html, 'html.parser')

	for num in range(1,7):
		print("Reemplazando titulo tema y resumen en p %d"%num)
		tag_titulo = sopa_index.find('a',{"id":"titulo_%d"%num})
		tag_titulo.string = dict_noticias[num][1]

		tag_tema = sopa_index.find('a',{"id":"tema_%d"%num})
		tag_tema.string = dict_noticias[num][2]
		
		tag_resumen = sopa_index.find('p',{"id": "resumen_%d"%num})
		tag_resumen.string = dict_noticias[num][4]

		tag_imagen = sopa_index.find('img',{"id": "imagen_%d"%num})
		tag_imagen["src"] = dict_noticias[num][3]

		reemplazardatosenpage(num)
	
	with open(html_fin, "wb") as f_output:
		f_output.write(sopa_index.prettify("utf-8"))

def reemplazardatosenpage(num):
	"""
	Reemplazar los datos de la noticia principal dentro de la subpagina
	"""
	html_ini = os.path.join(sourcesdir,'elBromercio/pages/noticia%d/index.html'%num)
	# ruta output desarrollo
	# html_fin = os.path.join(sourcesdir,'elBromercio/pages/single%d_copy.html'%num)
	# ruta output produccion
	html_fin = os.path.join(ruta_output,'pages/noticia%d/index.html'%num)
	
	html = open(html_ini) 
	sopa_single = BeautifulSoup(html, 'html.parser')

	tag_tema = sopa_single.find('a',{"class":"stuff_category"})
	tag_tema.string = dict_noticias[num][2]

	tag_titulo = sopa_single.find('a',{"id":"titulo"})
	tag_titulo.string = dict_noticias[num][1]

	tag_noticia = sopa_single.find('p',{"id":"noticia"})
	# tag_noticia.string = dict_noticias[num][5]
	tag_noticia.contents = dict_noticias[num][5]

	tag_imagen = sopa_single.find('img',{"id":"imagen_principal"})
	tag_imagen["src"] = dict_noticias[num][3]


	with open(html_fin, "wb") as f_output:
		f_output.write(sopa_single.prettify("utf-8"))

	




def main():
	get_premium_news()
	for i in range(1,7):

		url = dict_noticias[i][0]
		print(url)
		sopita = getSoupContent(url)
		time.sleep(2)
		tema, img_url = getSubjectandImage(sopita)
		print(tema)
		print(img_url)
		nameimg = "img_%d"%i
		# downloadfile(nameimg, img_url, imgsdir_output,'jpg')

		resumen, texto_noticia = getcontenido(sopita)
		# resumen = texto_noticia[0:248]+"..."
		dict_noticias[i].append(tema)
		dict_noticias[i].append(img_url)
		dict_noticias[i].append(resumen)
		dict_noticias[i].append(texto_noticia)
		print("*****************************")

	

if __name__ == '__main__':
	main()
	reemplazardatosenhtml()
