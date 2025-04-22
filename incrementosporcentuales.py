# contiene la función que calcula los incrementos porcentuales
import pandas as pd
def incrementoporcentual(df):
    tiendas = df['Store'].unique()
    listpd = []
    for store in tiendas:
        data = df[df['Store'] == store]
        df1 = data.copy()
        # Media movil
        df1.loc[:, 'Weekly_Sales media_movil'] =df1['Weekly_Sales'].rolling(window=3).mean()
        df1.loc[:, 'CPI media_movil'] =df1['CPI'].rolling(window=3).mean()
        df1.loc[:, 'Fuel_Price media_movil'] =df1['Fuel_Price'].rolling(window=3).mean()
        df1.loc[:, 'Temperature media_movil'] =df1['Temperature'].rolling(window=3).mean()
        df1.loc[:, 'Unemployment media_movil'] =df1['Unemployment'].rolling(window=3).mean()
        # Incremento porcentual
        df1.loc[:, 'Weekly_Sales cambio porcentual'] = 100 * abs((df1['Weekly_Sales'] - df1['Weekly_Sales media_movil']) / (df1['Weekly_Sales media_movil'])).round(4)
        df1.loc[:, 'CPI cambio porcentual'] = 100 * abs((df1['CPI'] - df1['CPI media_movil']) / (df1['CPI media_movil'])).round(4)
        df1.loc[:, 'Fuel_Price cambio porcentual'] = 100 * abs((df1['Fuel_Price'] - df1['Fuel_Price media_movil']) / (df1['Fuel_Price media_movil'])).round(4)
        df1.loc[:, 'Temperature cambio porcentual'] = 100 * abs((df1['Temperature'] - df1['Temperature media_movil']) / (df1['Temperature media_movil'])).round(4)
        df1.loc[:, 'Unemployment cambio porcentual'] = 100 * abs((df1['Unemployment'] - df1['Unemployment media_movil']) / (df1['Unemployment media_movil'])).round(4)
        listpd.append(df1)
    listpd = pd.concat(listpd,axis=0)
    
    listpdExp = listpd[['Date','Store','Weekly_Sales','Holiday_Flag','Temperature',
                        'Fuel_Price', 'CPI', 'Unemployment', 'Holiday_Events',
                        'Weekly_Sales cambio porcentual',
                        'CPI cambio porcentual',
                        'Fuel_Price cambio porcentual',
                        'Temperature cambio porcentual',
                        'Unemployment cambio porcentual']].copy()
    listpdExp = listpdExp.fillna(0)
    
    listpdExp['Date'] = pd.to_datetime(listpdExp['Date'], format='%Y-%m-%d')
    return listpdExp

# Función que agrega las ciudades al dataframe
def agg_City(Stores,df):
    Citys = Stores['City'].unique()
    citys_store = {City: [] for City in Citys}
    df['City'] = None
    for StoreID in Citys:
        ID = Stores[Stores['City'] == StoreID]['Store_ID'].to_list()
        df.loc[df['Store'].isin(ID), 'City'] = StoreID
        citys_store[StoreID].append(ID)
    return df

# función que calcula las ventas totales
def ventastotales(df):
    TotalSalesbyCity = df.groupby(by=['City']).agg(
        TotalSales = ('Weekly_Sales','sum'),
        MeanSales = ('Weekly_Sales','mean'),
        CountSales = ('Weekly_Sales','count'),
        StdSales = ('Weekly_Sales','std')
        ).assign(
            cv = lambda x: ((x['StdSales']/x['MeanSales'])*100)
        ).reset_index()
    TotalSalesbyCity = TotalSalesbyCity.sort_values(by='TotalSales', ascending=False)
    TotalSalesbyCity = TotalSalesbyCity.round(2)
    # agregamos las coordenadas de las ciudades
    city_coordinates = {
    "San Antonio": {"latitude": 29.4241, "longitude": -98.4936},
    "Los Angeles": {"latitude": 34.0522, "longitude": -118.2437},
    "Houston": {"latitude": 29.7604, "longitude": -95.3698},
    "Phoenix": {"latitude": 33.4484, "longitude": -112.0740},
    "New York": {"latitude": 40.7128, "longitude": -74.0060},
    "San Diego": {"latitude": 32.7157, "longitude": -117.1611},
    "Chicago": {"latitude": 41.8781, "longitude": -87.6298},
    "Philadelphia": {"latitude": 39.9526, "longitude": -75.1652}
    }
    coordinates_df = pd.DataFrame.from_dict(city_coordinates, orient='index').reset_index()
    coordinates_df.columns = ['City', 'Latitude', 'Longitude']
    TotalSalesbyCity = pd.merge(TotalSalesbyCity, coordinates_df, on='City', how='left')
    return TotalSalesbyCity