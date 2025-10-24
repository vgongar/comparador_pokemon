import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import create_pokemon_stats_visualization

def cosine_similarity(pokemon_name, n=7):
    """
    Devuelve la similaridad de cada Pokémon calculada a través del cosine similarity
    """
    # Obtenemos las estadísticas del pokémon:
    pokemon_row = stats[stats["name"] == pokemon_name]
    pokemon_stats = pokemon_row.drop(["id", "name"], axis = 1) # Eliminamos las columnas de id y de name
    pokemon_id = pokemon_row.index[0]

    numeric_stats = stats[stats.columns[2:8]]
    dot_sq = (numeric_stats @ pokemon_stats.T)**2
    uu = int((pokemon_stats**2).sum(axis=1)) # norma al cuadrado de las stats
    vv = (numeric_stats**2).sum(axis=1)
    
    result_df = pd.DataFrame(
        {
            "name": stats["name"],
            "metrica": dot_sq.values.flatten()/(uu*vv)
         }
    )

    return result_df.drop(pokemon_id).sort_values("metrica", ascending = False).head(n)

def euclidean_similarity(pokemon_name, n=7):
    """
    Devuelve la similaridad de cada Pokémon calculada a través de la distancia euclídea
    """
    # Obtenemos las estadísticas del pokémon:
    pokemon_row = stats[stats["name"] == pokemon_name]
    pokemon_stats = pokemon_row.drop(["id", "name"], axis = 1) # Eliminamos las columnas de id y de name
    pokemon_id = pokemon_row.index[0]

    numeric_stats = stats[stats.columns[2:8]]
    diff = numeric_stats - stats.drop(["id", "name"], axis = 1).loc[pokemon_id]
    
    distance = (diff**2).sum(axis=1)

    result_df = pd.DataFrame(
        {
            "name": stats["name"],
            "metrica": distance
         }
    )

    return result_df.drop(pokemon_id).sort_values("metrica").head(n)

stats = pd.read_csv("pokemon_home.csv")

#st.dataframe(data=stats)
st.title("Comparador de Pokémon")

pokemon_name = st.selectbox(
    label = "Introduce el nombre de un Pokémon",
    options = stats.name
)

pokemon_row = stats[stats["name"] == pokemon_name]
pokemon_stats = pokemon_row.drop(["id", "name"], axis = 1)

image_col, chart_col = st.columns(2)
with image_col:
    st.image(f"sprites/{pokemon_name}.png")
with chart_col:
    st.pyplot(create_pokemon_stats_visualization(pokemon_stats.T))

metric_option = st.segmented_control(label="Métrica", options=["Coseno", "Euclídea"], default="Coseno")

if st.button(
    "Calcular!",
    help="Calcula el top de Pokémon con reparto de estadísticas más similar",
    type="primary",
    icon="🚀"
    ):
    if metric_option == "Coseno":
        top = cosine_similarity(pokemon_name)
    elif metric_option == "Euclídea":
        top = euclidean_similarity(pokemon_name)
    st.divider()
    for index in range(len(top)):
        name = top.iloc[index]['name']
        color = "yellow" if index == 0 else "grey" if index == 1 else "orange" if index == 2 else "blue"
        title_cols = st.columns(2)
        with title_cols[0]:
            st.badge(f"#{index+1}", color=color)
            st.title(f"{name.capitalize()}")
        with title_cols[1]:
            st.write(f"{top.iloc[index]['metrica']:.4f}")
        pokemon_col, stat_col = st.columns(2)
        
        with pokemon_col:
            st.image(f"sprites/{name}.png")
        with stat_col:
            st.pyplot(
                create_pokemon_stats_visualization(
                    stats[stats["name"] == name].drop(["id", "name"], axis = 1).T
                    )
            )
        
        st.divider()