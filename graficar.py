# Funciónes que gráfican
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px



#---------------------- Gráficas de series de tiempo--------------------------#
def plot_timeserie(df, user_input):
    data = df.set_index('Date', drop=True).copy()
    data = data[data['Store'] == user_input['Store']]
    
    # Crear la figura con subgráficos
    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.1,
        row_heights=[0.5, 0.35, 0.15],
        specs=[[{"type": "scatter"}], [{"type": "scatter"}], [{"type": "box"}]]
    )
    
    # Nuevos colores con mejor contraste
    color_serie = '#1F77B4'  # Azul oscuro
    color_cambio = '#D62728'  # Rojo oscuro
    color_boxplot = '#2CA02C'  # Verde oscuro
    
    # Gráfico 1: Serie temporal
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data[user_input['variable']], 
        mode='lines', 
        name=user_input['variable'], 
        line=dict(color=color_serie, width=1.5),
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.2)'  # Versión semitransparente del color principal
    ), row=1, col=1)
    
    # Gráfico 2: Incremento Porcentual
    fig.add_trace(go.Scatter(
        x=data.index, 
        y=data[user_input['variable'] + ' cambio porcentual'],
        mode='lines', 
        name='Incremento %', 
        line=dict(color=color_cambio, width=1.5),
        fill='tozeroy',
        fillcolor='rgba(214, 39, 40, 0.2)'
    ), row=2, col=1)
    
    # Gráfico 3: Boxplot del Incremento Porcentual (horizontal)
    fig.add_trace(go.Box(
        x=data[user_input['variable'] + ' cambio porcentual'], 
        name='',
        boxpoints='outliers',
        marker=dict(
            color=color_boxplot, 
            outliercolor='#7F7F7F',  # Gris para outliers
            line=dict(width=1.2)
        ),
        line=dict(color=color_boxplot)
    ), row=3, col=1)
    
    # Configuración del diseño
    fig.update_layout(
        height=350, 
        width=300,
        title_text="Visualización de variables temporales en tiendas",
        title_font=dict(size=20, family="Arial Bold", color='#333333'),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='top',
            y=-0.15,
            xanchor='center',
            x=0.5,
            font=dict(color='#333333')
        ),
        font=dict(size=14, color='#333333'),  # Texto en gris oscuro
        margin=dict(l=70, r=20, t=50, b=70),
        plot_bgcolor='white',
        paper_bgcolor='white',
    )
    
    # Configuración de ejes
    for row in [1, 2, 3]:
        fig.update_yaxes(
            row=row, col=1,
            title_standoff=10,
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.5)',  # Gris claro para la grilla
            title_font=dict(color='#333333'),
            tickfont=dict(color='#333333')
        )
        
    fig.update_xaxes(
        showgrid=True,
        gridcolor='rgba(200, 200, 200, 0.5)',
        tickformat='%Y-%m',
        title_font=dict(color='#333333'),
        tickfont=dict(color='#333333')
    )
        # Etiquetas de los ejes X
    fig.update_xaxes(title_text="", row=1, col=1, title_standoff=10, 
                 showgrid=True, gridcolor='lightgray', showticklabels=True)
    fig.update_xaxes(title_text="", row=2, col=1, title_standoff=10, 
                     showgrid=True, gridcolor='lightgray', showticklabels=True)

    # Formatear las fechas en los ejes X
    fig.update_xaxes(tickformat='%Y-%m', row=1, col=1)  # Formato de fecha para el gráfico 1
    fig.update_xaxes(tickformat='%Y-%m', row=2, col=1)  # Formato de fecha para el gráfico 2
    
    # Etiquetas específicas
    fig.update_yaxes(title_text=user_input['variable'], row=1, col=1)
    fig.update_yaxes(title_text="Incre %", row=2, col=1)
    fig.update_yaxes(title_text="Boxplot", row=3, col=1)
    
    return fig

def plot_towserie(df,modelo_seleccionado):
    # Crear la figura con subgráficos
    df = df.sort_index()
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.1,  # Menos separación entre gráficos
        row_heights=[0.7, 0.7],  # Ajustar proporción de cada gráfico (70% y 30%)
        specs=[[{"type": "scatter"}], [{"type": "scatter"}]]
    )
    fig.add_trace(go.Scatter(x=df.index,
                            y=df['Weekly_Sales'], 
                            mode='lines', name= 'Ventas semanales', 
                            line=dict(color='#00BFFF', width=1.5)
                        ), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index,
                        y=df[modelo_seleccionado +'pred'], 
                        mode='lines', name= 'Predicciones', 
                        line=dict(color='red', width=1.5)
                    ), row=1, col=1)
    # gráfico de correlación
    correlacion = df['Weekly_Sales'].corr(df[modelo_seleccionado + 'pred'])
    fig.add_trace(go.Scatter(
        x=df['Weekly_Sales'],
        y=df[modelo_seleccionado + 'pred'],
        mode='markers',
        marker=dict(
            color='#2ca02c',  # Verde
            size=8,
            opacity=0.6,
            line=dict(width=1, color='DarkSlateGrey')
        ),
        hovertemplate=
            'Ventas reales: %{x:.0f}$<br>' +
            'Predicción: %{y:.0f}$<br>' +
            f'Correlación: {correlacion:.4f}<extra></extra>',
        showlegend=False
    ), row=2, col=1)

    # Añadir línea de 45 grados para referencia
    fig.add_shape(
        type="line",
        x0=min(df['Weekly_Sales']),
        y0=min(df['Weekly_Sales']),
        x1=max(df['Weekly_Sales']),
        y1=max(df['Weekly_Sales']),
        line=dict(color="red", width=2, dash="dash"),
        row=2, col=1
    )

    # Actualizar diseño general
    fig.update_layout(
        title='<b>Ventas vs predicciones</b>',
        title_font=dict(size=20, family='Arial', color='black'),
        font=dict(family='Arial', size=12, color='black'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=400,
        margin=dict(l=50, r=50, b=50, t=80),
        hovermode='x unified'
    )
    # Actualizar ejes
    fig.update_xaxes(
        title_text='<b>Fecha</b>',
        title_font=dict(color='black'),
        tickfont=dict(color='black'),
        showgrid=True,
        gridcolor='lightgray',
        row=1, col=1
    )
    fig.update_yaxes(
        title_text='<b>Ventas Semanales</b>',
        title_font=dict(color='black'),
        tickfont=dict(color='black'),
        showgrid=True,
        gridcolor='lightgray',
        row=1, col=1
    )

    fig.update_xaxes(
        title_text='<b>Ventas Reales</b>',
        title_font=dict(color='black'),
        tickfont=dict(color='black'),
        showgrid=True,
        gridcolor='lightgray',
        row=2, col=1
    )

    fig.update_yaxes(
        title_text='<b>Predicciones</b>',
        title_font=dict(color='black'),
        tickfont=dict(color='black'),
        showgrid=True,
        gridcolor='lightgray',
        row=2, col=1
    )
    fig.update_xaxes(title_text="", row=1, col=1, title_standoff=10, 
                showgrid=True, gridcolor='lightgray', showticklabels=True)
    fig.update_xaxes(tickformat='%Y-%m', row=1, col=1)
    return fig

#---------------------- Gráficas de pie char, bar--------------------------#
# función para graficar pie char, retorna paleta de colores 
def plotpiechar(dataset, names, values, labels, hovertemplate, texttemplate, title):
    pie_fig = px.pie(
        dataset, 
        names=names, 
        values=values,
        title=title,
        hole=0.3,
        labels=labels,
        height=320,
        width=700
    )

    pie_fig.update_traces(
        textinfo='value',
        textposition='inside',
        textfont=dict(size=12, weight="bold"),
        hovertemplate=hovertemplate,
        texttemplate=texttemplate,
        marker=dict(line=dict(color='#FFFFFF', width=1)),
        domain=dict(x=[0.0, 0.8])  # Esto asegura que el gráfico esté centrado y deja espacio para la leyenda
    )

    pie_fig.update_layout(
        title_font=dict(size=20, family='Arial', color='#333333', weight='bold'),
        legend=dict(
            orientation='v',
            yanchor='middle',
            y=0.5,
            xanchor='left',
            x=0.0,  # Esto coloca la leyenda fuera del gráfico, a la derecha
            font=dict(size=12, family='Arial', weight='bold')
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=150, t=80, b=50),  # Ajusta r para dejar espacio a la derecha
    )

    pie_colors = pie_fig['data'][0]['marker']['colors']
    return pie_fig, pie_colors
""" llamar de la siguiente forma:
    pie_fig, pie_colors = plotpiechar(dataset,names ='City',values='TotalSales',
                                    labels={'TotalSales': 'Ventas'},
                                    hovertemplate='<b>%{label}</b><br>Ventas: %{value:.0f} mil M<extra></extra>',  # Formato con un decimal al pasar el mouse
                                    texttemplate='%{value:.0f}mil M',  # Formato con un decimal dentro de las porciones,
                                    title='Ventas por ciudad')
"""

# función para graficar digramas de barras, recibe paleta de colores del grafico piechar
def plotbar(dataset,pie_colors,Y,X,Labels,texttemplate,Title):
        
        bar_fig = px.bar(
            dataset,
            y=Y,
            x=X,
            orientation='h',
            labels=Labels,
            title=Title,
            color='City',
            color_discrete_sequence=pie_colors,
            text_auto='.2f',
            height=320,
            #width=600
            )
        bar_fig.update_traces(
            texttemplate=texttemplate,  # Formato con negrita y símbolo %
            #textposition='outside',  # Opcional: ajusta la posición del texto
            )
        bar_fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',  # Fondo blanco
            paper_bgcolor='rgba(0,0,0,0)',  # Área del gráfico blanca
            title_x=0.5,  # Título centrado
            title_font=dict(size=18, family='Arial', color='black', weight='bold'),  # Negrita añadida
            xaxis=dict(
                title_font=dict(size=14, family='Arial', color='black', weight='bold'),  # Negrita añadida
                tickfont=dict(size=12, family='Arial', color='black', weight = 'bold'),
                showgrid=True,
                gridcolor='lightgrey',
                zerolinecolor='lightgrey',
            ),
            yaxis=dict(
                title='',  # Eliminamos el título del eje Y ya que son las ciudades
                tickfont=dict(size=12, family='Arial', color='black', weight='bold'),  # Negrita añadida para las etiquetas del eje Y
                autorange="reversed",  # Para que la ciudad con mayor valor quede arriba
                ticklen=10,
                showline=True,  # Muestra la línea del eje Y
                linecolor='black',
                automargin=True,  # Ajuste automático de márgenes
                ticksuffix="   ",  
            ),
            
            hoverlabel=dict(
                bgcolor='white',
                font_size=12,
                font_family='Arial'
            ),
            showlegend=False,  # Ocultamos la leyenda ya que ya tenemos las etiquetas
            bargap=0.2,
        )
        return bar_fig
""" 
llamar la función de la siguiente forma:
    bar_fig = plotbar(dataset,pie_colors,Y ='City',X='cv',
                Labels={'cv': 'Porcentaje de variación'},
                texttemplate ='<b>%{x:.2f}%</b>', # muestra 2 decimales y el simbolo %
                Title=''

                )
"""

#-------------------------- función que grafica el mapa------------------------#
def plotmap(dataset,pie_colors,mapbox_style):
        map_fig = px.scatter_mapbox(
        dataset,
        lat='Latitude',
        lon='Longitude',
        hover_name='City',
        hover_data=['TotalSales', 'cv'],
        color='City',
        color_discrete_sequence=pie_colors,
        size=[15]*len(dataset),
        zoom=3,
        #width=560,
        height=240
        #title='<b>Ubicación de las Ciudades</b>'
        )

        map_fig.update_layout(
            mapbox_style=mapbox_style,
            margin={"r":0,"t":40,"l":0,"b":0},
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',  # Fondo transparente del área del gráfico
            plot_bgcolor='rgba(0,0,0,0)',   # Fondo transparente del área de trazado
            legend=dict(
                orientation="h",  # Horizontal
                yanchor="bottom",  # Anclar al fondo
                y=1.09,  # Posicionar arriba del gráfico
                xanchor="center",  # Centrar horizontalmente
                x=0.5,  # Posición central
                font=dict(size=10,weight="bold")  # Texto en negrita
                ),
                title_font=dict(weight="bold"),
                hoverlabel=dict(font=dict(weight="bold"))
            )
        return map_fig

""" Llamar de la siguiente forma:
map_fig = plotmap(dataset,pie_colors,mapbox_style="open-street-map")
"""

# Aquí está la función que grafica las predicciones y el diagrama de barras
def plotseriebar(df,y,Labels,texttemplate,Title):
    # agrupemos los datos por meses:
    df['month'] = df.index.month_name()
    grupo_meses = df.groupby('month')[y].sum().reset_index()

    # Crear la figura con subgráficos
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.1,  # Menos separación entre gráficos
        row_heights=[0.7, 0.7],  # Ajustar proporción de cada gráfico (70% y 30%)
        specs=[[{"type": "scatter"}], [{"type": "bar"}]]
    )
    fig.add_trace(go.Scatter(x=df.index,
                            y=df[y], 
                            mode='lines', name= 'Predicciones semanales', 
                            line=dict(color='#00BFFF', width=1.5)
                        ), row=1, col=1)
    
    # crear el diagrama de barras
    colores = [
        '#B4DE72',  
        '#F46DBC',  
        '#26D2E4',  
        '#F9A541',  
        '#925AD6',  
        '#26D487',  
        '#F05A42',  
        '#5252F2'   
    ]
    fig.add_trace(
        go.Bar(
            x=grupo_meses[y]/1e6,
            y=grupo_meses['month'],
            name='Total por mes',
            marker_color= colores[:len(grupo_meses)],
            orientation='h',
            text=grupo_meses[y].round(2),  # Texto en las barras
            texttemplate=texttemplate,  # Formato negrita
            textposition='auto',  # Posición automática del texto
            hovertemplate=
                    'Mes: %{y}<br>' +
                    'Ventas totales: %{x:.0f} Mill<br>'
        ),
        row=2, col=1
    )
    fig.update_layout(
         title='<b>Predicciones semanales</b>',
         title_font=dict(size=20, family='Arial', color='black'),
         font=dict(family='Arial', size=12, color='black'),
         plot_bgcolor='white',
         paper_bgcolor='white',
         legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
         height=350,
         #width=300
         margin=dict(l=50, r=50, b=50, t=80),
         hovermode='x unified'
    )
    # configuración de estilo para la serie de tiempo
    fig.update_xaxes(
         title_text='<b>Fecha</b>',
         title_font=dict(size=14, color='black', weight='bold'),
         tickfont=dict(size=12, color='black'),
         showgrid=True,
         gridcolor='lightgray',
         row=1, col=1
    )

    fig.update_yaxes(
        title_text='<b>Predicciones</b>',
        title_font=dict(size=14, color='black', weight='bold'),
        tickfont=dict(size=12, color='black'),
        showgrid=True,
        gridcolor='lightgray',
        row=1, col=1
    )

    # --- Eje X (barras) ---
    fig.update_xaxes(
        title_text="Total de ventas esperadas",
        title_font=dict(size=14, family='Arial', color='black', weight='bold'),
        tickfont=dict(size=12, family='Arial', color='black', weight='bold'),
        showgrid=True,
        gridcolor='lightgrey',
        zerolinecolor='lightgrey',
        row=2, col=1
    )
    # --- Eje Y (barras) ---
    fig.update_yaxes(
        title_text='',
        tickfont=dict(size=12, family='Arial', color='black', weight='bold'),
        autorange="reversed", 
        showline=True,
        linecolor='black',
        row=2, col=1
    )
    fig.update_xaxes(title_text="", row=1, col=1, title_standoff=10, 
                showgrid=True, gridcolor='lightgray', showticklabels=True)
    fig.update_xaxes(tickformat='%Y-%m-%d',tickfont=dict(weight='bold'), row=1, col=1)
    fig.update_yaxes(tickfont=dict(weight='bold'), row=1, col=1)
    return fig