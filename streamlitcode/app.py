import streamlit as st
from GetData import visual_one_airport, visual_busy_cities, visual_busy_airports, bar_busy_cities
from GetData import bar_busy_routes, visual_clustering, show_codependence
from DataFrames import data



st.title('Анализ данных FlightRadar24 об авиаперелетах')
st.text('Данный сайт является игрушкой, в которой можно смотреть информацию о мировых')
st.text('авиаперевозках. Все данные указаны за неделю.')
st.subheader('На карте можно увидеть все маршруты из данного аэропорта по его коду.')
iata = st.text_input('Выбранный код аэропорта IATA:', 'SVO')
st.text('')
visual_one_airport(iata)
st.text(' ')


#Визуализация загруженных городов
st.subheader('Данная карта показывает самые загруженные города в регионе')
region = st.selectbox('Выберите регион',
                      ('usa', 'asia', 'europe', 'north america', 'south america', 'africa'))
st.text(' ')
visual_busy_cities(region)
st.text(' ')


#Статистика загруженных аэропортов
st.subheader('Самые загруженные аэропорты мира')
st.text(' ')
visual_busy_airports()
st.text(' ')


#Статистика загруженных городов по странам
st.subheader('Самые загруженные города стран мира')
country = st.selectbox('Выбранная страна:', ['All']+sorted(data['Departure_country'].unique()))
num = int(st.text_input('Выбранное количество городов:', 25))
st.text(' ')
bar_busy_cities(num, country)
st.text(' ')


#Статистика загруженных маршрутов
st.subheader('Самые загруженные маршруты мира')
n = int(st.text_input('Выбранное количество маршрутов:', 20))
st.text(' ')
bar_busy_routes(n)
st.text(' ')


#Кластеризация
st.subheader('Спектральная кластеризация аэропортов')
n_clusters = int(st.text_input('Выбранное количество кластеров (рекомендуемое количество 180):', 180))
st.text(' ')
visual_clustering(n_clusters)
st.text(' ')


#codependence
st.subheader('Созависимость стран')
st.text('Созависимость учитывает какую долю перелетов страны A составляют перелеты в')
st.text('страну B. Но также учитывается какую долю перелетов страны B составляют перелеты')
st.text('в страну A.')
country = st.selectbox('Выбранная страна:', sorted(data['Departure_country'].unique()))
st.text(' ')
show_codependence(country)
st.text(' ')
