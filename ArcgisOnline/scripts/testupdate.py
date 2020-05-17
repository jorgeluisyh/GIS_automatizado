import os, requests
import json, uuid

def consulta_esquema(url):
    url = f'{url}/query'
    response = requests.post(
        url,
        data = {
        'where': '1=1',
        'outFields': "*",
        # 'returnCountOnly': 'true',
        'f': 'pjson'
        }
    )
    res = json.loads(response.text)
    pretty =json.dumps(res, indent=4)
    return res

def actualizar_servicio(url,datos):
    url_update = f'{url}/updateFeatures'
    #borramos geometría de la actualizacion
    for row in datos["features"]:
        del row["geometry"]
    
    res_update = requests.post(
        url_update,
        data = {
        'features': json.dumps(datos["features"]),
        # 'returnCountOnly': 'true',
        'f': 'pjson'
        }
    )
    resup = json.loads(res_update.text)
    print(resup)

def actualizar_datos(urlservicio,datosres):
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
  
    for x in range(len(datosres["features"])):
        identificador =datosres["features"][x]["attributes"]["Nombre_en"]

        for y in range(len(res2["features"])):
            m2 =res2["features"][y]["attributes"]
            name = m2["Country_Region"]

            if name == identificador:
                confirmed = m2["Confirmed"]
                deaths = m2["Deaths"]
                recovered = m2["Recovered"]
                active = m2["Active"]

                datosres["features"][x]["attributes"]["Nombre_es"]    = "testworkflow"

                # datosres["features"][x]["attributes"]["Sum_Confirmed"] = str(confirmed)
                # datosres["features"][x]["attributes"]["Sum_Deaths"]    = str(deaths)
                # datosres["features"][x]["attributes"]["Sum_Recovered"] = str(recovered)
                # datosres["features"][x]["attributes"]["Sum_Active"]    = str(active)        
                print(name, ":", "test")
    
    return datosres

def main(url_propio,url_datos):
    esquema = consulta_esquema(url_propio)
    datosactualizados =actualizar_datos(url_datos,esquema)
    actualizar_servicio(url_propio,datosactualizados)


if __name__ == '__main__':
    url_covid = 'https://services1.arcgis.com/0MSEUqKaxRlEPj5g/ArcGIS/rest/services/ncov_cases/FeatureServer/2'
    url_propio = 'https://services6.arcgis.com/LLutPLesjvi5h66l/ArcGIS/rest/services/borrar/FeatureServer/0'
    main(url_propio,url_covid)