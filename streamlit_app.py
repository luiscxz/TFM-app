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
from predicciones import parapredicciones,dataset_minmaxdata,generate_data_to_predict,forescatig
from incrementosporcentuales import incrementoporcentual,agg_City,ventastotales
from graficar import plot_timeserie,plotpiechar,plot_towserie,plotseriebar
import time
from datetime import date
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

modelos = {
    'XGBRegressor':xgb ,
    'RandomForestRegressor': random_forest,
    'GradientBoostingRegressor':gradient_boosting,
    'escalador':escalador
}
#---------------------------Fin lectura datos y modelo----------------------------------------#

# -------------------------Para la sección de ventas totales----------------------------------#
df = incrementoporcentual(df) # calcula incrementos porcentuales
df = agg_City(Stores,df) # agrega las ciudades al dataframe df
ventastotales = ventastotales(df)
ventastotales['TotalSales'] = ventastotales['TotalSales']/1e9
ventastotales['MeanSales'] = ventastotales['MeanSales']/1e6
# ---------------------------------------------------------------------------------------------#
dminmaxdf =dataset_minmaxdata(df)
def run_dash():
    subprocess.Popen(["python", "Dashboard.py"])
run_dash()

st.set_page_config(layout="wide")  # Configuración inicial
#1. Menú
def main():
    menu = ['Inicio','Series por tienda','Ventas totales por ciudad',
            'Análisis temporal','Modelado predictivo',
            'Forecasting']
    eleccion = st.sidebar.radio('Menú:', menu)
    #-----------------------------Lógica condicional-----------------------------#
    if eleccion=='Inicio':
        st.header('Sistema de pronóstico de ventas semanales')
        st.warning("""
        **ℹ️ Información del proyecto**

        Este proyecto consiste en un sistema iterativo diseñado para analizar los datos históricos 
        de ventas (2010-2012) de 45 tiendas ubicadas en Estados Unidos. La plataforma permite a los 
        usuarios generar predicciones comerciales mediante modelos de machine learning implementados en Python, 
        incluyendo RandomForestRegressor, GradientBoostingRegressor y XGBRegressor.

        **Secciones disponibles:**

        - **Series por tienda**: Visualización de la evolución temporal de las variables en cada tienda.
        - **Ventas totales por ciudad**: Análisis regional de las ventas que incluye el total por ciudad, la variabilidad entre ellas, los promedios correspondientes y su representación geográfica.
        - **Análisis temporal**: Exploración de las ventas anuales y mensuales por tienda y ciudad.
        - **Modelado predictivo**: Comparación entre las ventas observadas y las predicciones generadas por los modelos aplicados.
        - **Forecasting**: Herramienta que permite seleccionar un rango de fechas para generar proyecciones de ventas futuras..
        """)
    
    # -----------------Sección donde se visualizan las series temporales--------------------#
    #                                      serie por tienda                                 #
    #---------------------------------------------------------------------------------------#
    elif eleccion=='Series por tienda':
        col_store, col_variable = st.columns([4, 1])
        #------------------------ Diseño selección de tienda------------------------#
        with col_store:
            with st.container(border=True): # contenedor con borde
                st.markdown(
                            """
                            <style>
                                .titulo-tienda {
                                    font-size: 10px;
                                    font-weight: bold;
                                    margin-bottom: -30px;  /* Reduce espacio debajo del texto */
                                }
                            </style>
                            <p class="titulo-tienda">Seleccione una tienda:</p>
                            """,
                            unsafe_allow_html=True
                        )
                tienda_seleccionada = 1 
                # Mostrar botones en cuadrícula (5 filas x 9 columnas)
                total_tiendas = 45
                num_columnas = 15
                num_filas = 3
                # definimos estilo de botones
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
            with st.container(border=True):
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
        col_serie1, col_r = st.columns([3,1])
        with col_serie1:
            with st.container(border=True):
                fig = plot_timeserie(df, user_input)
                st.plotly_chart(fig, use_container_width=True,
                            config={
                                'displayModeBar': True,  # Mantener la barra de herramientas
                                'staticPlot': False,     # Permitir interactividad
                                'doubleClick': 'reset',  # Resetear con doble click
                                'displaylogo': False,    # Ocultar logo de Plotly
                                'modeBarButtonsToRemove': ['lasso2d', 'select2d', 'autoScale2d']
                            })
    
    # -----------------Sección donde se visualizan ventas totales por ciudad----------------#
    #                                      ventas totales                                   #
    #---------------------------------------------------------------------------------------#
    
    elif eleccion == 'Ventas totales por ciudad':
        # Ejecutar dasboard aquí
        time.sleep(2)
        #st.markdown("""<iframe src="http://127.0.0.1:8050/" width="100%" height="800" frameborder="0"></iframe>""", unsafe_allow_html=True)
        components.html("""
        <iframe src="https://dasboardtotfm.onrender.com" width="100%" height="100%" frameborder="0" style="position: absolute; top: 0; left: 0; right: 0; bottom: 0;"></iframe>""", 
        height=800)

    # -----------------Sección donde se visualizan el análisis temporal---------------------#
    #                                      ventas anuales y mensuales                       #
    #---------------------------------------------------------------------------------------#
    elif eleccion =='Análisis temporal':
        ciudades = ventastotales['City'].to_list()
        colum_city, colum_store = st.columns([1, 3])
        col_pie_ventas_anuales, colpie_ventas_mensuales = st.columns([1, 1])
        with colum_city:
            with st.container(border=True):
                ciudad_seleccionada = st.radio(
                    "Selecciona una variable:",
                    options=ciudades,
                    index=0,  # Opción seleccionada por defecto 
                    key="radio_ciudad"
                )
                # almacenamos la ciudad
                
                store_city = df[df['City']==ciudad_seleccionada]['Store'].unique()        

        with colum_store:
            with st.container(border=True):
                st.markdown(
                            """
                            <style>
                                .titulo-tienda {
                                    font-size: 10px;
                                    font-weight: bold;
                                    margin-bottom: -30px;  /* Reduce espacio debajo del texto */
                                }
                            </style>
                            <p class="titulo-tienda">Seleccione una tienda:</p>
                            """,
                            unsafe_allow_html=True
                        )
                tienda_seleccionada = 1 
                # Mostrar botones en cuadrícula (5 filas x 9 columnas)
                total_tiendas = len(store_city)
                num_columnas = 3
                num_filas = 4
                # definimos estilo de botones
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
                        tienda_idx = col_idx * num_filas + fila
                        if tienda_idx < total_tiendas:
                            numero_tienda = store_city[tienda_idx]  # Obtiene el número de tienda
                            if cols[col_idx].button(str(numero_tienda)):
                                tienda_seleccionada = numero_tienda  # Almacena el número seleccionad
        # almacenamos los valores seleccionados, en este caso ciudad y tienda
        seleccion = {'City':ciudad_seleccionada,
                    'Store':tienda_seleccionada}
        #----------------- Filtrado y agrupación del dataframe-----------------------------#
        condicion = ((df['City'] == seleccion['City']) & (df['Store'] == seleccion['Store']))
        data = df[condicion]
        data = data.set_index('Date',drop=True)
        data['Año'] = data.index.year
        data['month'] = data.index.month
        meses_es = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }
        data['month'] = data['month'].map(meses_es)  # Aplica el mapeo
        # agrupemos por año
        grupaños = data.groupby(by=['Año']).agg(
            cantidad = ('Weekly_Sales','count')
        ).reset_index()

        # Agrupemos por mes
        grupmes = data.groupby(by=['month']).agg(
            cantidad = ('Weekly_Sales','count')
        ).reset_index()
        #--------------------------------- Piechar--------------------------#


        with col_pie_ventas_anuales:
            with st.container(border=True):
                pie_figy, _ = plotpiechar(grupaños,names ='Año',values='cantidad',
                                        labels={'Año': 'Año', 'cantidad': 'Ventas'},
                                        hovertemplate='<b>%{label}</b><br>Cantidad de ventas: %{value:.0f} <extra></extra>',  # Formato con un decimal al pasar el mouse
                                        texttemplate='%{value:.0f}',  # Formato con un decimal dentro de las porciones,
                                        title='Ventas Anuales')
                
                pie_figy.update_layout(
                    legend=dict(
                    orientation='v',
                    yanchor='middle',
                    y=0.5,
                    xanchor='left',
                    x=1.0,  # Esto coloca la leyenda fuera del gráfico, a la derecha
                    font=dict(size=12, family='Arial', weight='bold')))
                st.plotly_chart(pie_figy, use_container_width=True,
                                config={
                                    'displayModeBar': False,  # Mantener la barra de herramientas
                                    'staticPlot': False,     # Permitir interactividad
                                    'doubleClick': 'reset',  # Resetear con doble click
                                    'displaylogo': False,    # Ocultar logo de Plotly
                                    'modeBarButtonsToRemove': ['lasso2d', 'select2d', 'autoScale2d']})
        
        with colpie_ventas_mensuales:
            with st.container(border=True):
                pie_figm, _ = plotpiechar(grupmes,names ='month',values='cantidad',
                                        labels={'Mes': 'month', 'cantidad': 'Ventas'},
                                        hovertemplate='<b>%{label}</b><br>Cantidad de ventas: %{value:.0f} <extra></extra>',  # Formato con un decimal al pasar el mouse
                                        texttemplate='%{value:.0f}',  # Formato con un decimal dentro de las porciones,
                                        title='Ventas Mensuales')
                pie_figm.update_layout(
                    legend=dict(
                    orientation='v',
                    yanchor='middle',
                    y=0.5,
                    xanchor='left',
                    x=1.0,  # Esto coloca la leyenda fuera del gráfico, a la derecha
                    font=dict(size=12, family='Arial', weight='bold')))
                st.plotly_chart(pie_figm, use_container_width=True,
                                config={
                                    'displayModeBar': False,  # Mantener la barra de herramientas
                                    'staticPlot': False,     # Permitir interactividad
                                    'doubleClick': 'reset',  # Resetear con doble click
                                    'displaylogo': False,    # Ocultar logo de Plotly
                                    'modeBarButtonsToRemove': ['lasso2d', 'select2d', 'autoScale2d']})
                                    
                  
    # -----------------Sección donde se visualizan las predicciones del los modelos---------#
    #                                      datos reales vs predicciones                     #
    #---------------------------------------------------------------------------------------#
    elif eleccion == 'Modelado predictivo':
        col_stores, col_models = st.columns([2.5, 1])                      
        with col_models:
                modelos_list =['XGBRegressor','RandomForestRegressor','GradientBoostingRegressor']
                with st.container(border=True):
                    modelo_seleccionado = st.radio(
                        "Selecciona un modelo:",
                        options=modelos_list,
                        index=0,  # Opción seleccionada por defecto 
                        key="radio_modelos"
                    )
                    # Llamamos la función para que haga las predicciones
                    df_p = parapredicciones(df,modelos,modelo_seleccionado) 
        with col_stores:
            with st.container(border=True): # contenedor con borde
                st.markdown(
                            """
                            <style>
                                .titulo-tienda {
                                    font-size: 10px;
                                    font-weight: bold;
                                    margin-bottom: -30px;  /* Reduce espacio debajo del texto */
                                }
                            </style>
                            <p class="titulo-tienda">Seleccione una tienda:</p>
                            """,
                            unsafe_allow_html=True
                        )
                tienda_seleccionada1 = 1
                # Mostrar botones en cuadrícula (5 filas x 9 columnas)
                total_tiendas = 45
                num_columnas = 15
                num_filas = 3
                # definimos estilo de botones
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
                                tienda_seleccionada1 = tienda_id                
                                #st.dataframe(df_p)
        user_input2 ={
        'Store':tienda_seleccionada1}
        df_p = df_p[df_p['Store']==user_input2['Store']]
        # Sección donde se grafican las predicciones de los modelos y los datos reales.
        col_serie, col_correlation = st.columns([3,1])
        with col_serie:
            fig_orinalvspred =plot_towserie(df_p,modelo_seleccionado)
            st.plotly_chart(fig_orinalvspred, use_container_width=True,
                            config={
                            'displayModeBar': True,  # Mantener la barra de herramientas
                            'staticPlot': False,     # Permitir interactividad
                            'doubleClick': 'reset',  # Resetear con doble click
                            'displaylogo': False,    # Ocultar logo de Plotly
                            'modeBarButtonsToRemove': ['lasso2d', 'select2d', 'autoScale2d']
                        })

    elif eleccion == 'Forecasting':
        col_stores, col_models = st.columns([2.5, 1])                           
        with col_models:
                modelos_list =['XGBRegressor','RandomForestRegressor','GradientBoostingRegressor']
                with st.container(border=True):
                    modelo_seleccionado = st.radio(
                        "Selecciona un modelo:",
                        options=modelos_list,
                        index=0,  # Opción seleccionada por defecto 
                        key="radio_modelos"
                    )

        with col_models:
                with st.container(border=True):
                    selected_date = st.date_input(
                        "Selecciona una fecha:",
                        min_value=date(2012,10,26),
                        max_value=date(2012, 12, 28),  # Fecha actual por defecto
                        key="selector_fecha"
                    )
                    # --- Validación y corrección automática ---
                    if selected_date.weekday() != 4:  # Si no es viernes
                        st.warning("¡Solo se permiten viernes! Vuelve a seleccionar la fecha")

                    else:
                        st.success("✅ Fecha válida (viernes)")
                        fecha ={'fecha':selected_date}
                        st.write(selected_date)
        input_date ={'Fecha_usuario':selected_date.strftime('%Y-%m-%d')}
        with col_stores:
            with st.container(border=True): # contenedor con borde
                st.markdown(
                            """
                            <style>
                                .titulo-tienda {
                                    font-size: 10px;
                                    font-weight: bold;
                                    margin-bottom: -30px;  /* Reduce espacio debajo del texto */
                                }
                            </style>
                            <p class="titulo-tienda">Seleccione una tienda:</p>
                            """,
                            unsafe_allow_html=True
                        )
                tienda_seleccionada1 = 1
                # Mostrar botones en cuadrícula (5 filas x 9 columnas)
                total_tiendas = 45
                num_columnas = 15
                num_filas = 3
                # definimos estilo de botones
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
                                tienda_seleccionada1 = tienda_id  
        variables_df= generate_data_to_predict(dminmaxdf,input_date)
        #obtenemos las predicciones
        dfSelect = forescatig(variables_df,modelos,modelo_seleccionado)
        dfSelect = dfSelect[dfSelect['Store']==tienda_seleccionada1]
        with col_stores:
            with st.container(border=True):
                colums = str(dfSelect.filter(like='pred').columns[0])
                
                fig_p =plotseriebar(dfSelect,colums,
                                    Labels={'Ventas': 'Total ventas'},
                                    texttemplate ='<b>%{x:.0f}Mill</b>',
                                    Title='')

                st.plotly_chart(fig_p, use_container_width=True,
                            config={
                            'displayModeBar': True,  # Mantener la barra de herramientas
                            'staticPlot': False,     # Permitir interactividad
                            'doubleClick': 'reset',  # Resetear con doble click
                            'displaylogo': False,    # Ocultar logo de Plotly
                            'modeBarButtonsToRemove': ['lasso2d', 'select2d', 'autoScale2d']
                        })

if __name__ == "__main__":
    main()  
