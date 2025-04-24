# predicciones en datos conocidos
import pandas as pd
import numpy as np
def parapredicciones(df,modelos,modelo_seleccionado):
    data = df.copy()
    data['week'] = data['Date'].dt.isocalendar().week
    # leyendo fechas del segmentador
    fecha_inicio = data['Date'].min()
    fecha_fin = data['Date'].max()

    dfSelect = data[data['Date'].between(fecha_inicio, fecha_fin)]
    
    dfSelect = dfSelect[['Weekly_Sales', 'Store', 'CPI', 'Unemployment', 'Holiday_Events','week']]
    
    # cargamos los modelos
    modelo = modelos[modelo_seleccionado]
    escalador = modelos["escalador"]
    
    # Prepara y transforma los datos para los modelos.
    X = dfSelect.drop(columns=['Weekly_Sales'], axis=1)
    Xs = pd.DataFrame(escalador.transform(X),
                     columns = X.columns,
                     index = X.index)
    
    # Agregamos las predicciones de los modelos
    dfSelect[modelo_seleccionado +'pred'] = modelo.predict(Xs).astype(int)
    dfSelect['Date'] = data['Date']
    dfSelect = dfSelect.set_index('Date',drop=True)
    return dfSelect

# función calcula los valores mínimos y máximos.
def dataset_minmaxdata(df):
    data = df.copy()
    data['week'] = data['Date'].dt.isocalendar().week
    data = data[['Store','CPI','Unemployment','Holiday_Events','week','Date']]
    data = data.set_index('Date',drop=True)
    # Para cada tienda, consultemos el CPI y Unemployment mínimo y máximo.
    dicc = {
        'Store':[],
        'CPI_min':[],
        'CPI_max':[],
        'Unemployment_min':[],
        'Unemployment_max':[]
        }
    for store in data['Store'].unique():
        dicc['Store'].append(store)
        dicc['CPI_min'].append(data[data['Store'] == store]['CPI'].min())
        dicc['CPI_max'].append(data[data['Store'] == store]['CPI'].max())
        dicc['Unemployment_min'].append(data[data['Store'] == store]['Unemployment'].min())
        dicc['Unemployment_max'].append(data[data['Store'] == store]['Unemployment'].max())
    df_dicc = pd.DataFrame(dicc)
    return df_dicc

# función para generar los datos que se usarán en las predicciones.
def generate_data_to_predict(df_dicc,input_date):
    variables ={
    'Date':[],
    'Store':[],
    'CPI':[],
    'Unemployment':[],
    'Holiday_Events':[]
    }
    np.random.seed(42)
    date_range = pd.date_range(start='2012-10-26',end=input_date['Fecha_usuario'],freq='W-FRI')
    num_dates = len(date_range)
    for store in df_dicc['Store']:
        variables['Date'].extend(date_range)
        variables['Store'].extend([store]*num_dates) # repite la tienda 
        variables['CPI'].extend(np.random.uniform(df_dicc[df_dicc['Store']==store]['CPI_min'],
                                                df_dicc[df_dicc['Store']==store]['CPI_max'],num_dates))
        variables['Unemployment'].extend(np.random.uniform(df_dicc[df_dicc['Store']==store]['Unemployment_min'],
                                                        df_dicc[df_dicc['Store']==store]['Unemployment_max'],num_dates))
        variables['Holiday_Events'].extend(np.random.randint(0,2,num_dates))
    variables_df = pd.DataFrame(variables)
    #variables_df['week'] = variables_df['Date'].dt.isocalendar().week
    #variables_df = variables_df.set_index('Date',drop=True)
    return variables_df

#función forescating
def forescatig(df,modelos,modelo_seleccionado):
    data = df.copy()
    data['week'] = data['Date'].dt.isocalendar().week
    dfSelect = data[['Store', 'CPI', 'Unemployment', 'Holiday_Events','week']]
    # cargamos los modelos
    modelo = modelos[modelo_seleccionado]
    escalador = modelos["escalador"]
    # Prepara y transforma los datos para los modelos.
    # cargamos los modelos
    modelo = modelos[modelo_seleccionado]
    escalador = modelos["escalador"]
    # Prepara y transforma los datos para los modelos.
    Xs = pd.DataFrame(escalador.transform(dfSelect),
                     columns = dfSelect.columns,
                     index = dfSelect.index)
    
    # Agregamos las predicciones de los modelos
    dfSelect[modelo_seleccionado +'pred'] = modelo.predict(Xs).astype(int)
    dfSelect['Date'] = data['Date']
    dfSelect = dfSelect.set_index('Date',drop=True)
    return dfSelect