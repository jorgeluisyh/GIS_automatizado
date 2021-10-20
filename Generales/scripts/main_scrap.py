#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

dict_noticias= dict()


diario = "https://elcomercio.pe"
res = requests.get(diario)
contenido = res.content
sopa = BeautifulSoup(contenido,'html.parser')
tag = 'a'
clase = 'featured-story__title-link title-xs line-h-sm overflow-hidden'

mydivs = sopa.find_all(tag, {"class": clase})

for num, div in enumerate(mydivs, 1):
	dict_noticias[num]= diario+div["href"]


def getimage(url_noticia):
	tag = 'img'
	clase = "s-multimedia__image w-full o-cover s-multimedia__image--big"
	res = requests.get(url_noticia)
	contenido = res.content
	sopa = BeautifulSoup(contenido,'html.parser')
	# print sopa.prettify('utf-8')
	imgdiv = sopa.find_all(tag,{"class": clase})[0]
	imgurl = imgdiv["src"]
	return imgurl

def getcontenido(url_noticia):
    res = requests.get(url)
    contenido = res.content
    sopa = BeautifulSoup(contenido,'html.parser')
    titulo = sopa.find('title').get_text()
    print(titulo.encode('utf-8'))

    x=sopa.find_all(['h2','p'])




for i in range(1,7):
	url = dict_noticias[i]
	print(url)
	print(getimage(url))