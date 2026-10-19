import requests
import urllib.parse

key = "265c67a4-4cb5-41ae-8e4f-b819e68976a1" 

route_url = "https://graphhopper.com/api/1/route?"
geocode_url = "https://graphhopper.com/api/1/geocode?"

def geocoding(location, key):
    # Esta función busca las coordenadas de la ciudad que ingreses
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    respuesta = requests.get(url)
    json_data = respuesta.json()
    status = respuesta.status_code
    
    if status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        return status, lat, lng, name
    else:
        return status, None, None, None

print("=== Programa de Rutas de la Biblioteca Nacional ===")
print("Escriba 's' o 'salir' en cualquier momento para terminar el programa.\n")

while True:
    loc1 = input("Lugar de Origen: ")
    if loc1.lower() == "s" or loc1.lower() == "salir":
        print("Saliendo del programa...")
        break
    orig = geocoding(loc1, key)

    loc2 = input("Destino: ")
    if loc2.lower() == "s" or loc2.lower() == "salir":
        print("Saliendo del programa...")
        break
    dest = geocoding(loc2, key)

    print("=================================================")
    if orig[0] == 200 and dest[0] == 200 and orig[1] and dest[1]:
        # Formatear coordenadas para la URL de ruta
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": "car", "locale": "es"}) + op + dp
        paths_status = requests.get(paths_url)
        paths_data = paths_status.json()

        if paths_status.status_code == 200:
            print("Indicaciones desde {} hasta {}".format(orig[3], dest[3]))
            
            dist_km = paths_data["paths"][0]["distance"] / 1000.0
            time_sec = paths_data["paths"][0]["time"] / 1000.0
            time_min = time_sec / 60.0
            
            print(f"Distancia Viajada: {dist_km:.2f} km")
            print(f"Duración del Viaje: {time_min:.2f} minutos")
            print("=================================================")
            print("Narrativa del viaje paso a paso:")
            
            for instruccion in paths_data["paths"][0]["instructions"]:
                texto_ruta = instruccion["text"]
                distancia_ruta = instruccion["distance"] / 1000.0
                print(f" - {texto_ruta} ( {distancia_ruta:.2f} km )")
            print("=================================================\n")
        else:
            print("Error: No se pudo encontrar una ruta entre esos dos puntos.\n")
    else:
        print("Lugar no encontrado. Por favor, verifique los nombres e intente nuevamente.\n")