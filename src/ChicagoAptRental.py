import gmaps
import sys
import os
import pymongo
sys.path.append('/Users/dipakrimal/work/')
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pymongo import MongoClient
from scipy import stats
from scipy.stats import norm
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_absolute_error
from sklearn.externals import joblib
import plotly.plotly as py
import plotly.graph_objs as go
from neighborhoods import gps_to_neighborhood
import warnings
warnings.filterwarnings("ignore")

def load_data():
    MONGO_URI = "mongodb+srv://drimal:05152012@cluster0-jxt6i.mongodb.net/test?retryWrites=true"
    client = MongoClient(MONGO_URI)
    db = client.cglistings
    collection = db.housing
    df = pd.DataFrame(list(collection.find()))
    return df
    

def preprocess_data_columns(df):
    df['baths'] = df['baths'].replace('Ba', '').astype('float')
    df['price'] = df['price'].replace('$', '').astype('float')
    df = df[['link', 'title', 'postdate', 'latitude', 'longitude', 'neighborhood', \
        'beds', 'baths', 'area', 'others', 'price']]
    return df

def plot_missing_info(df, output_location='../visualizations'):
    missing_df = df.isnull().sum(axis=0).reset_index()
    missing_df.columns = ['column_name', 'missing_count']
    missing_df = missing_df.ix[missing_df['missing_count'] > 0]
    ind = np.arange(missing_df.shape[0])
    width = 0.9
    fig, ax = plt.subplots(figsize=(12, 8))
    rects = ax.barh(ind, missing_df.missing_count.values, color='b')
    ax.set_yticks(ind)
    ax.set_yticklabels(missing_df.column_name.values, rotation='horizontal')
    ax.set_xlabel("Count of missing values")
    ax.set_title("Number of missing values in each column")
    plt.savefig(output_fig_location+'/missing_value_in_columns.png)

def make_count_plots(df, column, xlimit=10, ):
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.countplot(x=column, data=df)
    plt.xlim(0, xlimit)
    plt.savefig('../visualizations/count_plots_%s.png', %column)
    
def remove_outliers(df):
    df = df[(df['beds'] < 10)]
    df = df[(df['price'] < 10000) & (df['price'] > 100)]
    return df
    
def plot_price_heatmap(df):
    APIKEY = os.getenv('GMAPAPIKEY')
    gmaps.configure(api_key=APIKEY)
    fig = gmaps.figure()
    df['location'] = df.apply(lambda x: (x['latitude'], x['longitude']), axis=1)
    locations = df['location']
    weights = df['price'].values
    #locations = (df['latitude'], df['longitude'])
    heatmap_layer = gmaps.heatmap_layer(locations, weights=weights)
    heatmap_layer.max_intensity = 2000
    heatmap_layer.point_radius = 30
    fig.add_layer(heatmap_layer)
    fig.savefig('../visualizations/price_heatmap.png')


def get_distance_from_union_station(lon2, lat2):
    # convert decimal degrees to radians
    lon1 = -87.6403
    lat1 = 41.8787
    lon1, lat1, lon2, lat2 = map(np.deg2rad, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 3956  # Radius of earth in miles
    return c * r


@click.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True, dir_okay=False))
@click.argument('output_file', type=click.Path(writable=True, dir_okay=False))
@click.option('--excel', type=click.Path(writable=True, dir_okay=False))



def main(input_file, output_file, excel):
    
    print('Preparing data')

    df = load_data()
    df = preprocess_data_columns(df)


    
if __name__ == __