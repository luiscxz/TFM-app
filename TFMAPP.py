# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 15:11:02 2025
APP en streamlit TFM
@author: Luis A. García
"""
import streamlit as st
import subprocess
import streamlit.components.v1 as components
import pandas as pd
import pickle
from datetime import date
from incrementosporcentuales import incrementoporcentual,agg_City,ventastotales
from graficar import plot_timeserie
#-----------------------------Lectura del dataframe -----------------------------#
df = pd.read_csv('WalmartSalesClean.csv')
Stores = pd.read_csv('TFM_Table_Store.csv', delimiter = ';')

#-----------------Lectura de modelos 
with open("modelos.pkl", "rb") as file:
    modelos = pickle.load(file)
xgb = modelos["XGBRegressor"]
random_forest = modelos["RandomForestRegressor"]
gradient_boosting = modelos["GradientBoostingRegressor"]
escalador = modelos["escalador"]
#---------------------------Fin lectura datos y modelo----------------------------------------#

# ventas por ciudad
df = incrementoporcentual(df) # calcula incrementos porcentuales
df = agg_City(Stores,df) # agrega las ciudades al dataframe df
ventastotales = ventastotales(df)
ventastotales['TotalSales'] = ventastotales['TotalSales']/1e9
ventastotales['MeanSales'] = ventastotales['MeanSales']/1e6
dataset = ventastotales.copy()

st.set_page_config(layout="wide")  # Configuración inicial
#1. Menú
def main():
    menu = ['Inicio','Series por tienda','Ventas totales por ciudad',
            'Análisis temporal','Modelado predictivo',
            'Forecasting']
    eleccion = st.sidebar.radio('Menú:', menu)
    #-----------------------------Lógica condicional-----------------------------#
    if eleccion=='Inicio':
        st.header('Bienvenido al proyecto de predicción de Ventas Semanales')
        st.warning("""
        **ℹ️ Información del proyecto**

        Este proyecto tiene como objetivo predecir las ventas semanales de 45 tiendas en Estados Unidos, 
        utilizando modelos de machine learning como **RandomForestRegressor**, **GradientBoostingRegressor** y **XGBRegressor** desarrollados en Python, 
        a partir de datos recopilados entre 2010 y 2012.

        **Secciones disponibles:**

        - **Series por tienda**: Visualización de las series temporales de las variables analizadas para cada tienda.
        - **Ventas totales por ciudad**: Análisis del total de ventas, variabilidad relativa, promedio por ciudad y su ubicación geográfica.
        - **Análisis temporal**: Exploración de las ventas anuales y mensuales por tienda y ciudad.
        - **Modelado predictivo**: Comparación entre las ventas reales y las predicciones generadas por los modelos.
        - **Forecasting**: Permite seleccionar un rango de fechas para generar pronósticos de ventas futuros.
        """)
    
    # -----------------Sección donde se visualizan las series temporales-----------------#
    elif eleccion=='Series por tienda':
        col_store, col_variable = st.columns([4, 1])  
        #------------------------ Diseño selección de tienda------------------------#
        with col_store:
            st.markdown("**Seleccione una tienda:**")
            tienda_seleccionada = 1 
            # Mostrar botones en cuadrícula (5 filas x 9 columnas)
            total_tiendas = 45
            num_columnas = 15
            num_filas = 3
            button_style = """
            <style>
                div[data-testid="column"] {
                    padding: 0 !important;  /* Elimina el padding de las columnas */
                }
                button[kind="secondary"] {
                    height: 40px !important;
                    width: 100% !important;
                    font-size: 16px !important;
                    padding: 0 !important;
                    margin: 0 !important;  /* Elimina márgenes externos */
                    border: 1px solid #ccc !important;  /* Opcional: mantiene el borde visible */
                }
                /* Reduce el espacio entre columnas */
                [data-testid="column"] {
                    margin: 0 -1px !important;  /* Columnas se superponen ligeramente */
                }
            </style>
            """
            st.markdown(button_style, unsafe_allow_html=True)
            # Crear las columnas
            cols = st.columns(num_columnas)
            # Llenar la cuadrícula con el patrón vertical
            for col_idx in range(num_columnas):
                for fila in range(num_filas):
                    tienda_id = col_idx * num_filas + fila + 1
                    if tienda_id <= total_tiendas:
                        if cols[col_idx].button(str(tienda_id)):
                            tienda_seleccionada = tienda_id


        #------------------------ Diseño selección de variable----------------------#
        with col_variable:
            st.subheader("Variables")
            series = ["Fuel_Price", "Temperature", "Unemployment", "Weekly_Sales"]
            serie_seleccionada = st.radio(
                "Selecciona una variable:",
                options=series,
                index=0,  # Opción seleccionada por defecto (CPI)
                key="radio_series"
            )

        #---------------------------------------------------------------------------#
        # Guardemos los datos de entrada en un diccionario
        user_input ={
            'Store':tienda_seleccionada,
            'variable':serie_seleccionada
        }
        
        with st.container():
            fig = plot_timeserie(df, user_input)
            st.plotly_chart(fig, use_container_width=True,
                        config={
                            'displayModeBar': True,  # Mantener la barra de herramientas
                            'staticPlot': False,     # Permitir interactividad
                            'doubleClick': 'reset',  # Resetear con doble click
                            'displaylogo': False,    # Ocultar logo de Plotly
                            'modeBarButtonsToRemove': ['lasso2d', 'select2d', 'autoScale2d']
                        })
    
    # -----------------Sección donde se visualizan las ventas totales-----------------#
    
    elif eleccion == 'Ventas totales por ciudad':
        # Ejecutar dasboard aquí
        def run_dash():
            subprocess.Popen(["python", "Dashboard.py"])
        run_dash()
        
        #st.markdown("""<iframe src="http://127.0.0.1:8050/" width="100%" height="800" frameborder="0"></iframe>""", unsafe_allow_html=True)
        components.html("""
        <iframe src="http://127.0.0.1:8050/" width="100%" height="100%" frameborder="0" style="position: absolute; top: 0; left: 0; right: 0; bottom: 0;"></iframe>""", 
        height=800)

    #     
if __name__ == "__main__":
    main()  # Permite ejecutar tests en Spyder
