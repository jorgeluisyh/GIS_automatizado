import os, requests
import json, uuid

_USER = 'adminsam'
_PASSWORD = 'cristal2016%'
token_gis = ''

def getToken():
    '''
    :return: Devuelve el token unico por modulo y maquina 
    '''
    global token_gis
    _URL = "https://www.arcgis.com/sharing/generateToken"
    data = {
        'username': _USER,
        'password': _PASSWORD,
        'referer': "https://www.arcgis.com",
        'request': 'gettoken',
        'f': 'json'
    }
    response = requests.post(_URL, data=data)
    response = response.json()
    token = response.get('token', 0)
    token_gis = token


def consulta_esquema(url):
    """
    Consulta de esquema de nuestro servicio en el agol y retornamos los datos en formato json
    params:
        url: url del servicio
    outputs:
        res: datos del servicio en formato json
    """
    url = f'{url}/query'
    response = requests.post(
        url,
        data = {
        'where': '1=1',
        'outFields': "*",
        # 'returnCountOnly': 'true',
        'token': token_gis,
        'f': 'pjson'
        }
    )
    res = json.loads(response.text)
    pretty =json.dumps(res, indent=4)
    return res

def actualizar_servicio(url,datos):
    """
    Actualizar los datos de nuestro servicio con los datos obtenidos de la API en formato json
    params:
        url: url del servicio propio
        datos: datos obtenidos de la API en formato json

    """
    url_update = f'{url}/updateFeatures'
    #borramos geometría de la actualizacion
    for row in datos["features"]:
        del row["geometry"]
    
    res_update = requests.post(
        url_update,
        data = {
        'features': json.dumps(datos["features"]),
        # 'returnCountOnly': 'true',
        'token': token_gis,
        'f': 'pjson'
        }
    )
    print(datos)
    resup = json.loads(res_update.text)
    print(resup)

def actualizar_datos(urlservicio,datosres):
    """
    Actualizamos los datos del json de con los datos obtenidos de la API
    params:
        urlservicio: url del servicio de datos
        datosres: datos vacios contiene el esquema de nuestro servicio a actualizar
    outputs:
        datosres: datos actualizados con los datos obtenidos de la API
    """
    url = f'{urlservicio}/query'
    response2 = requests.post(
        url,
        data = {
        'where': '1=1',
        'outFields': "*",
        # 'returnCountOnly': 'true',
        'f': 'pjson'
        }
    )
    res2 = json.loads(response2.text)
    
    numpaises = len(res2["features"])
    print("el numero de registros es: {}".format(str(numpaises)))
  
    for x in range(len(datosres["features"])):
        identificador =datosres["features"][x]["attributes"]["Nombre_en"]

        for y in range(len(res2["features"])):
            m2 =res2["features"][y]["attributes"]
            name = m2["Country_Region"]

            if name == identificador:
                confirmed = m2["Confirmed"] if m2["Confirmed"]!=None else -1
                deaths = m2["Deaths"] if m2["Deaths"]!=None else -1
                recovered = m2["Recovered"] if m2["Recovered"]!=None else -1
                # active = m2["Active"] if m2["Active"]!=None else -1


                # datosres["features"][x]["attributes"]["Nombre_es"]    = "prueba"

                datosres["features"][x]["attributes"]["confirmado"] = str(confirmed)
                datosres["features"][x]["attributes"]["muertes"]    = str(deaths)
                datosres["features"][x]["attributes"]["recuperado"] = str(recovered)
                # datosres["features"][x]["attributes"]["Sum_Active"]    = str(active)        
    
    return datosres

def main(url_propio,url_datos):
    getToken()
    print('token: {}'.format(token_gis))
    print("leemos el esquema de datos")
    esquema = consulta_esquema(url_propio)
    print("obtenemos los datos del servicio a actualizar")
    datosactualizados =actualizar_datos(url_datos,esquema)
    print("actualizamos los datos de nuestro servicio")
    actualizar_servicio(url_propio,datosactualizados)


if __name__ == '__main__':
    url_covid = 'https://services1.arcgis.com/0MSEUqKaxRlEPj5g/ArcGIS/rest/services/ncov_cases/FeatureServer/2'
    # url_propio = 'https://services6.arcgis.com/LLutPLesjvi5h66l/ArcGIS/rest/services/sudamerica_covid_19/FeatureServer/0'
    url_propio = 'https://services6.arcgis.com/Hp9VjF6h55A4WBre/ArcGIS/rest/services/paises_sudamerica/FeatureServer/0'
    main(url_propio,url_covid)