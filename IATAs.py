import country_converter
import airportsdata
import pandas as pd
import numpy as np


#Делаем словарик с IATA-ми
airportscoords = airportsdata.load()

def get_iatas():
    #Создаем словарь для перевода IATA аэропорта в всю интересующую нас информацию
    iata_info = {}
    for icao in airportscoords.keys():
        iata_info[airportscoords[icao]['iata']] = {'name': airportscoords[icao]['name'],
                                                   'city': airportscoords[icao]['city'],
                                                   'country': airportscoords[icao]['country'],
                                                   'lat': airportscoords[icao]['lat'],
                                                   'lon': airportscoords[icao]['lon'],
                                                   'tz': airportscoords[icao]['tz']}

    #Используем еще один датасет, т.к. данный не знает много аэропортов
    iatas = pd.read_csv('iatas.csv')
    iatas = iatas.to_dict()

    for row in iatas['code'].keys():
        if not (iatas['code'][row] in iata_info.keys()):
            iata_info[iatas['code'][row]] = {'name': iatas['name'][row],
                                             'city': iatas['city_code'][row],
                                             'country': iatas['country_id'][row],
                                             'lon': iatas['location'][row].split()[1][1:],
                                             'lat': iatas['location'][row].split()[2][:-1],
                                             'tz': iatas['time_zone_id'][row]}

    #Почему-то в пакете Намибия превратилась в nan, видимо, человеческая ошибка. Меняем это.
    for i in iata_info.keys():
        if iata_info[i]['country'] is np.nan:
            iata_info[i]['country'] = 'Namibia'

    return iata_info
iata_info = get_iatas()

def translate_counties():
    #все страны для перевода из двоичного названия в нормальное
    countrydict ={}

    abbrv_countries = []
    for i in iata_info.keys():
        abbrv_countries.append(iata_info[i]['country'])

    for abbrv in set(abbrv_countries):
        countrydict[abbrv] = country_converter.convert(abbrv, to = 'name_short')



    for iata in iata_info.keys():
        iata_info[iata]['country'] = countrydict[iata_info[iata]['country']]

    return iata_info
iata_info = translate_counties()