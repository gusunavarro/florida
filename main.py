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

    # Opciones de gráficos
    chart_type = st.selectbox("Elige el tipo de gráfico", ['Barras', 'Torta', 'Lineal', 'Scatter'])

    if chart_type == 'Barras':
        # Crear un gráfico de barras
        plt.figure(figsize=(10, 6))
        sns.barplot(x=x_column, y=y_column, data=df)
        st.pyplot(plt)
    elif chart_type == 'Torta':
        # Crear un gráfico de torta si y_column es seleccionable
        pie_data = df[y_column].value_counts()
        plt.figure(figsize=(8, 8))
        plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
        st.pyplot(plt)
    elif chart_type == 'Lineal':
        # Crear un gráfico lineal
        plt.figure(figsize=(10, 6))
        sns.lineplot(x=x_column, y=y_column, data=df)
        st.pyplot(plt)
    elif chart_type == 'Scatter':
        # Crear un gráfico de dispersión
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=x_column, y=y_column, data=df)
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

        
        
        
