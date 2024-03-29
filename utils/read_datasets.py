from sklearn import datasets
import pandas as pd

Dsource_dir = './data_source/'

def read_sklearn_datasets(ds_name):
    if ds_name == 'iris':
        ds = datasets.load_iris()
    elif ds_name == 'boston house-prices':
        ds = datasets.load_boston()
    ds_df = pd.DataFrame(ds.data, columns=ds.feature_names)

    return ds_df

def read_csv_datasets(ds_name):
    global Dsource_dir
    ds_df = pd.read_csv(Dsource_dir + ds_name + '.csv')

    return ds_df