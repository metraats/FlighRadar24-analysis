import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import networkx as nx
import numpy as np
from Clustering import G


from DataFrames import data, total_flights_by_city, total_flights_by_airports, most_busy_routes
from DataFrames import create_airports_df



#Функция для создания маршрутов для одного аэропорта
def visual_one_airport(iata):
    ist = data[data['Departure'] == iata]

    #Точки, куда прилетает
    fig = px.scatter_geo(ist,
                         lat = 'Arrival_lat',
                         lon = 'Arrival_lon',
                         hover_name='Arrival_city',
                         projection='orthographic',
                         size = 'Number of flights')
    #Маршруты
    for i in range(len(ist)):
        fig.add_trace(
            go.Scattergeo(
                hoverinfo = 'text',
                text = ist['Arrival_city'].iloc[i],
                lon = [ist['Arrival_lon'].iloc[i], ist['Departure_lon'].iloc[i]],
                lat = [ist['Arrival_lat'].iloc[i], ist['Departure_lat'].iloc[i]],
                mode = 'lines',
                line = dict(width = 0.1, color = 'blue')
            )
        )
    #Стамбул
    fig.add_scattergeo(lat = ist['Departure_lat'],
                       lon = ist['Departure_lon'],
                       hovertext = ist['Departure_city'])
    #layout
    fig.update_layout(margin=dict(l=3, r=3, t=0, b=0),
                      showlegend = False)

    st.plotly_chart(fig)

#Функция для отображения карты загруженности городов
def visual_busy_cities(region):
    fig = px.scatter_geo(total_flights_by_city[total_flights_by_city['number of flights'] > 200],
                             hover_name='city',
                             lat='lat',
                             lon = 'lon',
                             color = 'country',
                             size = 'number of flights'
                             )

    fig.update_layout(margin=dict(l=3, r=3, t=0, b=0),
                      showlegend = False,
                      geo = dict(scope = region))

    st.plotly_chart(fig)

#Загруженные аэропорты
def visual_busy_airports():
    fig = px.bar(total_flights_by_airports.sort_values()[-15:],
                 orientation='v',
                 height = 500)
    st.plotly_chart(fig)

#Загруженные города
def bar_busy_cities(num=25, country='All'):

    if country == 'All':
        total_flights_by_city.sort_values('number of flights', inplace=True)

        fig = px.bar(total_flights_by_city[-num:], x = 'number of flights', y = 'city',
                     orientation='h',
                     color = 'country',
                     height = 25*num+200)
    else:
        total_flights_by_city.sort_values('number of flights', inplace=True)

        fig = px.bar(total_flights_by_city[total_flights_by_city['country'] == country][-num:],
                     x = 'number of flights',
                     y = 'city',
                     orientation='h',
                     color = 'country',
                     height = 25*num,
                     title = 'Самые загруженные города мира')

    st.plotly_chart(fig)

#Загруженные маршруты
def bar_busy_routes(num=30):
    fig = px.bar(most_busy_routes[-num:], y = 'Number of flights', x = 'Route',
                 orientation = 'v',
                 height = 700)
    st.plotly_chart(fig)

#Визуал кластеризации
def visual_clustering(n_clusters):
    fig = px.scatter_geo(create_airports_df(n_clusters),
                         hover_name='airport',
                         lat='lat',
                         lon = 'lon',
                         color = 'label',
                         color_continuous_scale='edge'
                         )

    fig.update_layout(margin=dict(l=3, r=3, t=0, b=0),
                      showlegend = False)

    st.plotly_chart(fig)

#codependence
def show_codependence(country):
    airports = create_airports_df(2)
    codependence = pd.DataFrame(columns = ['country', 'codependence'])
    graph_countries = airports['country']

    for i in graph_countries.unique():
        S = np.array(G.nodes)[graph_countries == country]
        T = np.array(G.nodes)[graph_countries == i]

        if nx.normalized_cut_size(G, S, T) !=0:
            codependence = pd.concat([codependence, pd.DataFrame(columns = ['country', 'codependence'],
                                                                 data = [[i, nx.normalized_cut_size(G, S, T, weight = 'flights')]])])
    codependence.sort_values(by = 'codependence', inplace = True)
    fig = px.bar(codependence.iloc[-30:], y = 'codependence', x = 'country', orientation='v',
                 color = 'codependence',
                 color_continuous_scale = 'sunsetdark',
                 height = 500,
                 width = 900)
    st.plotly_chart(fig)