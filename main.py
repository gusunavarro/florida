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
uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df.head())  # Muestra las primeras filas del DataFrame

    # Opciones de gráficos
    chart_type = st.selectbox("Elige el tipo de gráfico", ['Barras', 'Torta', 'Lineal'])

    if chart_type == 'Barras':
        st.bar_chart(df.iloc[:, 0:2])  # Modifica según la estructura de tu DataFrame
    elif chart_type == 'Torta':
        pie_data = df.iloc[:, 0].value_counts()
        plt.figure(figsize=(8, 8))
        plt.pie(pie_data, labels=pie_data.index)
        st.pyplot(plt)
    elif chart_type == 'Lineal':
        st.line_chart(df.iloc[:, 0:2])  # Modifica según la estructura de tu DataFrame



    # Continuación de tu código existente...

    # Cargar y mostrar archivo de mapa (GeoJSON)
    uploaded_file_map = st.file_uploader("Elige un archivo de mapa (GeoJSON)", type="geojson")
    if uploaded_file_map is not None:
        gdf = gpd.read_file(uploaded_file_map)

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