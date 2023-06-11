import pandas as pd
import glob
from IATAs import iata_info
from Clustering import G, clustering, vertexes
import streamlit as st


#Получаем данные:
data = pd.DataFrame()
for file in glob.glob('/Airportcsvs/*.csv'):
    data = pd.concat([data, pd.read_csv(file)])
data.reset_index(drop=True, inplace=True)
data = data[data['Number of flights'] != 0]


#Создаем датафрейм data
def create_data_df(data):
    data = data[data['Departure'].isin(iata_info.keys()) & data['Arrival'].isin(iata_info.keys())]
    data['Departure_city'] = data['Departure'].apply(lambda x: iata_info[x]['city'])
    data['Arrival_city'] = data['Arrival'].apply(lambda x: iata_info[x]['city'])
    data['Departure_country'] = data['Departure'].apply(lambda x: iata_info[x]['country'])
    data['Arrival_country'] = data['Arrival'].apply(lambda x: iata_info[x]['country'])
    data['Departure_airport'] = data['Departure'].apply(lambda x: iata_info[x]['name'])
    data['Arrival_airport'] = data['Arrival'].apply(lambda x: iata_info[x]['name'])
    data['Departure_lat'] = data['Departure'].apply(lambda x: iata_info[x]['lat'])
    data['Arrival_lat'] = data['Arrival'].apply(lambda x: iata_info[x]['lat'])
    data['Departure_lon'] = data['Departure'].apply(lambda x: iata_info[x]['lon'])
    data['Arrival_lon'] = data['Arrival'].apply(lambda x: iata_info[x]['lon'])
    data['Departure_tz'] = data['Departure'].apply(lambda x: iata_info[x]['tz'])
    data['Arrival_tz'] = data['Arrival'].apply(lambda x: iata_info[x]['tz'])
    return data
data = create_data_df(data)


#Создаем датафрейм total_flights_by_airports
def create_total_flights_by_airports_df(data):
    total_flights_by_airports = (data.groupby('Arrival')['Number of flights'].sum() +
                                 data.groupby('Departure')['Number of flights'].sum())

    total_flights_by_airports.fillna(data.groupby('Arrival')['Number of flights'].sum(), inplace = True)
    total_flights_by_airports.fillna(data.groupby('Departure')['Number of flights'].sum(), inplace = True)
    return total_flights_by_airports
total_flights_by_airports = create_total_flights_by_airports_df(data)


#Создаем датафрейм total_flights_by_city
def create_total_flights_by_city_df(total_flights_by_airports):
    total_flights = pd.DataFrame(columns = ['iata','airport', 'lat', 'lon', 'number of flights', 'city', 'country'])
    total_flights['iata'] = total_flights_by_airports.index
    total_flights['number of flights'] = total_flights_by_airports.values
    total_flights['airport'] = total_flights['iata'].apply(lambda x: iata_info[x]['name'])
    total_flights['lat'] = total_flights['iata'].apply(lambda x: iata_info[x]['lat'])
    total_flights['lon'] = total_flights['iata'].apply(lambda x: iata_info[x]['lon'])
    total_flights['city'] = total_flights['iata'].apply(lambda x: iata_info[x]['city'])
    total_flights['country'] = total_flights['iata'].apply(lambda x: iata_info[x]['country'])
    total_flights['city'].loc[total_flights['city'] == ''] = total_flights[total_flights['city'] == '']['airport']

    total_flights_by_city = total_flights.drop_duplicates(subset = ['city',	'country'])[['city','country','lat','lon']].merge(
        total_flights.groupby(['country', 'city'], as_index=False)['number of flights'].sum())
    return total_flights_by_city
total_flights_by_city = create_total_flights_by_city_df(total_flights_by_airports)

#Создаем датафрейм most_busy_routes
def create_most_busy_routes_df():
    most_busy_routes= pd.DataFrame()
    most_busy_routes['Route'] = data['Departure_city'] + '-' + data['Arrival_city']
    most_busy_routes['Number of flights'] = (data + data.rename(columns =
                                                                {'Departure_city':'Arrival_city',
                                                                 'Arrival_city':'Departure_city'}))['Number of flights']
    most_busy_routes.sort_values('Number of flights', inplace = True)
    return most_busy_routes
most_busy_routes = create_most_busy_routes_df()

#Создаем датафрейм airports
@st.cache_data
def create_airports_df(n_clusters):
    labels = clustering(n_clusters)
    airports = pd.DataFrame()
    airports['label'] = labels
    airports['airport'] = list(vertexes)
    airports['lat'] = airports['airport'].apply(lambda x: iata_info[x]['lat'])
    airports['lon'] = airports['airport'].apply(lambda x: iata_info[x]['lon'])
    airports['number of flights'] = airports['airport'].apply(lambda x: G.degree(weight = 'flights')[x])
    airports['country'] = airports['airport'].apply(lambda x: iata_info[x]['country'])
    return airports

