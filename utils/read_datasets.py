from sklearn import datasets
import pandas as pd

def read_datasets(ds_name):
    if ds_name == 'iris':
        ds = datasets.load_iris()
    elif ds_name == 'boston house-prices':
        ds = datasets.load_boston()
    ds_df = pd.DataFrame(ds.data, columns=ds.feature_names)

    return ds_df