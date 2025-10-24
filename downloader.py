import os

print("Pokémon Sprite Downloader")
ruta = "sprites" # Ruta por defecto

while True: # Bucle para pedir al usuario una ruta para poner la carpeta donde irán los sprites

    ruta = input("Introduce la ruta de la carpeta que quieres crear: ").strip()

    # Si la ruta esta vacía por defecto la colocamos en la misma carpeta donde está el archivo
    if not ruta:
        print("Ruta por defecto...")
        ruta = "sprites"

    try:
        # Intentamos crear la carpeta
        os.makedirs(ruta, exist_ok=True)
        print(f"La carpeta '{ruta}' ha sido creada correctamente (o ya existía).")
        break  # Salimos del bucle si todo ha ido bien
    except FileExistsError:
        print(f"La carpeta '{ruta}' ya existe.")
    except OSError as e:
        # Capturamos errores típicos (permisos, ruta inválida, etc.)
        print(f"No se pudo crear la carpeta: {e}")
        print("Por favor, introduce otra ruta válida.\n")


import requests
import time

# URL base de la PokéAPI
POKEAPI_BASE = "https://pokeapi.co/api/v2/pokemon/"

# Lista para guardar los datos
datos_pokemon = []

# Número máximo de Pokémon a descargar
# Pon None para todos los disponibles
MAX_POKEMON = None

# 1. Obtener la lista de Pokémon
response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=10000")
lista = response.json()["results"]

cant_pokemon = len(lista)

if MAX_POKEMON:
    lista = lista[:MAX_POKEMON]

# 2. Recorrer cada Pokémon
for idx, poke in enumerate(lista, start=1):
    nombre = poke["name"]
    print(f"[{idx}/{cant_pokemon}] Procesando {nombre}...")

    try:
        resp = requests.get(poke["url"])
        if resp.status_code != 200:
            print(f"Error al obtener {nombre}: {resp.status_code}")
            continue
        info = resp.json()

        # Estadísticas base
        stats = {s["stat"]["name"]: s["base_stat"] for s in info["stats"]}

        # URL del sprite HOME
        sprite_home = info["sprites"]["other"]["home"]["front_default"]

        # Descargar sprite si existe
        if sprite_home:
            resp_img = requests.get(sprite_home)
            if resp_img.status_code == 200:
                archivo = os.path.join(ruta, f"{nombre}.png")
                with open(archivo, "wb") as f:
                    f.write(resp_img.content)

        # Guardar datos
        datos_pokemon.append({
            "id": info["id"],
            "name": nombre,
            "HP": stats.get("hp"),
            "attack": stats.get("attack"),
            "defense": stats.get("defense"),
            "special_attack": stats.get("special-attack"),
            "special_defense": stats.get("special-defense"),
            "speed": stats.get("speed"),
        })

        # Espera para no saturar la API
        time.sleep(0.5)

    except Exception as e:
        print(f"Error con {nombre}: {e}")

# 3. Guardar CSV
import pandas as pd
df = pd.DataFrame(datos_pokemon)
df.to_csv("pokemon_home.csv", index=False)
print("¡Descarga completada! CSV generado: pokemon_home.csv")