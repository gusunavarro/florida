# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

# Título de la aplicación
st.title('Análisis y Visualización de Datos')

# Cargar y mostrar archivo CSV
uploaded_file_csv = st.file_uploader("Elige un archivo CSV", type="csv", key="csv")

# Cargar y mostrar archivo de mapa (GeoJSON) 
uploaded_file_geojson = st.file_uploader("Elige un archivo de mapa (GeoJSON)", type="geojson", key="geojson")

if uploaded_file_csv is not None:
    df = pd.read_csv(uploaded_file_csv)
    st.write(df.head())  # Muestra las primeras filas del DataFrame

    # Permitir al usuario seleccionar las columnas X e Y
    x_column = st.selectbox("Selecciona la variable X", df.columns)
    y_column = st.selectbox("Selecciona la variable Y", df.columns)

   # Función para generar gráficos
def generar_graficos(df):
    st.sidebar.title("Opciones de Gráficos")
    tipo_grafico = st.sidebar.selectbox("Selecciona el tipo de gráfico",
                                        ["Barras", "Tortas", "Líneas", "Scatter", "Histograma"])
    columna = st.sidebar.selectbox("Selecciona la columna para el gráfico", df.columns)

    if tipo_grafico == "Barras":
        st.bar_chart(df[columna])
    elif tipo_grafico == "Tortas":
        plt.figure(figsize=(8, 8))
        plt.pie(df[columna].value_counts(), labels=df[columna].value_counts().index, autopct='%1.1f%%')
        st.pyplot(plt)
    elif tipo_grafico == "Líneas":
        st.line_chart(df[columna])
    elif tipo_grafico == "Scatter":
        if 'latitude' in df.columns and 'longitude' in df.columns:
            st.map(df)
        else:
            st.error(
                "El DataFrame no contiene las columnas 'latitude' y 'longitude' para un gráfico scatter geográfico.")
    elif tipo_grafico == "Histograma":
        plt.hist(df[columna], bins=15)
        plt.title(f"Histograma de {columna}")
        plt.xlabel(columna)
        plt.ylabel("Frecuencia")
        st.pyplot(plt)


if uploaded_file_geojson is not None:
    gdf = gpd.read_file(uploaded_file_geojson)

    # Convertir las geometrías a puntos (si no son puntos, ajusta según sea necesario)
    if gdf.geom_type.unique()[0] != 'Point':
        gdf['geometry'] = gdf.centroid

    # Extraer latitud y longitud
    gdf["latitude"] = gdf.geometry.y
    gdf["longitude"] = gdf.geometry.x

    # Crear un DataFrame para st.map que solo contenga las columnas de latitud y longitud
    df_for_st_map = gdf[["latitude", "longitude"]]

    # Usar st.map para visualizar los datos
    st.map(df_for_st_map)
