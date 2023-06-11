import networkx as nx
from sklearn.base import ClusterMixin
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
from IATAs import iata_info
import glob


#Получаем данные:
data = pd.DataFrame()
for file in glob.glob('/Users/artemijstankevic/PycharmProjects/pythonProject6/Airportcsvs/*.csv'):
    data = pd.concat([data, pd.read_csv(file)])
data.reset_index(drop=True, inplace=True)
data = data[data['Number of flights'] != 0]
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




#Множество вершин:
vertexes = set([*data['Departure'], *data['Arrival']])

#Граф и Лапласиан
G = nx.MultiGraph()
G.add_nodes_from(vertexes)
e = list(zip(data['Arrival'], data['Departure'], data['Number of flights']))
G.add_weighted_edges_from(e, weight = 'flights')
L = nx.laplacian_matrix(G)

#Кластеризация класс
class GraphClustering(ClusterMixin):
    def __init__(self, n_clusters=8, n_components=None, **kwargs):
        if n_components is None:
            n_components = n_clusters

        self.n_components = n_components
        self.kmeans = KMeans(n_clusters=n_clusters, **kwargs)

    def fit_predict(self, L, y=None):
        eigenvectors = self._generate_eigenvectors(L)
        labels = self.kmeans.fit_predict(eigenvectors[:, 1:])
        return labels

    def _generate_eigenvectors(self, L):
        if self.n_components is None:
            return np.linalg.eigh(L)[1]
        else:
            return np.linalg.eigh(L)[1][:,:self.n_components]

#Функция для кластеризации
def clustering(n_clusters=180):
    model = GraphClustering(n_clusters)
    labels = model.fit_predict(L.todense())
    return labels