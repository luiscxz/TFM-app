# Funciónes que gráfican
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px


#---------------------- Gráficas de series de tiempo--------------------------#
def plot_timeserie(df,user_input):
    data = df.set_index('Date', drop=True).copy()
    data = data[data['Store']==user_input['Store']]
    # Crear la figura con subgráficos
    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.1,  # Menos separación entre gráficos
        row_heights=[0.5, 0.35, 0.15],  # Ajustar proporción de cada gráfico
        specs=[[{"type": "scatter"}], [{"type": "scatter"}], [{"type": "box"}]]
    )
    
    # Gráfico 1: Serie 
    fig.add_trace(go.Scatter(x=data.index,
                             y=data[user_input['variable']], 
                             mode='lines', name=user_input['variable'], 
                             line=dict(color='#00BFFF', width=1.5),
                             fill='tozeroy',fillcolor='rgba(72, 61, 139, 0.4)'
                            ), row=1, col=1)
    # Gráfico 2: Incremento Porcentual
    fig.add_trace(go.Scatter(x=data.index, 
                             y=data[user_input['variable'] + ' cambio porcentual'], # ejemplo: CPI cambio porcentual
                             mode='lines', name='Incremento %', 
                             line=dict(color='#FFA500', width=1.5),
                             fill='tozeroy',fillcolor='rgba(255,165,0,0.4)'
                            ), row=2, col=1)
    # Gráfico 3: Boxplot del Incremento Porcentual (horizontal)
    fig.add_trace(go.Box(
        x=data[user_input['variable'] + ' cambio porcentual'], 
        name='',
        boxpoints='outliers',
        marker=dict(color='#32CD32', outliercolor='red', line=dict(width=1.2))
    ), row=3, col=1)
    
    # Configuración del diseño
    fig.update_layout(
        height=400, width=300,  # Aumentar tamaño para mejor visualización
        title_text="Análisis de Series Temporales",
        title_font=dict(size=20, family="Arial Bold"),  # Fuente más grande
        showlegend=True,
        legend=dict(
            orientation='h',  # Leyenda horizontal
            yanchor='top',
            y=-0.15,  # Ajuste para que quede bien alineada debajo de los gráficos
            xanchor='center',
            x=0.5
        ),
        font=dict(size=14),  # Tamaño general de fuente
        margin=dict(l=70, r=20, t=50, b=70),  # Ajustar márgenes para evitar solapamientos
        plot_bgcolor='white',  # Fondo blanco
        paper_bgcolor='white',  # Fondo blanco
    )
    
    # Etiquetas de los ejes Y con alineación correcta
    fig.update_yaxes(title_text=user_input['variable'], row=1, col=1, title_standoff=10, showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(title_text="Incre %", row=2, col=1, title_standoff=10, showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(title_text="Boxplot", row=3, col=1, title_standoff=10, showgrid=True, gridcolor='lightgray')
    
    # Etiquetas de los ejes X
    fig.update_xaxes(title_text="", row=1, col=1, title_standoff=10, 
                 showgrid=True, gridcolor='lightgray', showticklabels=True)
    fig.update_xaxes(title_text="", row=2, col=1, title_standoff=10, 
                     showgrid=True, gridcolor='lightgray', showticklabels=True)

    # Formatear las fechas en los ejes X
    fig.update_xaxes(tickformat='%Y-%m', row=1, col=1)  # Formato de fecha para el gráfico 1
    fig.update_xaxes(tickformat='%Y-%m', row=2, col=1)  # Formato de fecha para el gráfico 2
    # Elimnar grilla 
    fig.update_xaxes(showgrid=False, row=1, col=1)  # Grilla vertical (fila 1)
    fig.update_xaxes(showgrid=False, row=2, col=1)  # Grilla vertical (fila 2)
    fig.update_yaxes(showgrid=False, row=1, col=1)  # Grilla horizontal (fila 1)
    fig.update_yaxes(showgrid=False, row=2, col=1)  # Grilla horizontal (fila 2)
    #fig.show()
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
