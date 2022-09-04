import os
import numpy as np
import pandas as pd

from sklearn.neighbors import NearestNeighbors
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def find_nearest_neighbors(distance_df, neighbors=3):
    nbrs = NearestNeighbors(n_neighbors=neighbors + 1, algorithm='ball_tree').fit(distance_df)
    distances, indices = nbrs.kneighbors(distance_df)
    distance_df = pd.DataFrame(distances)
    distance_df = distance_df.drop(0, axis=1)
    distance_df = distance_df.add_prefix('distance_')
    print(distance_df)

    index_df = pd.DataFrame(indices)
    index_df = index_df.drop(0, axis=1)
    index_df = index_df.add_prefix('index_')
    print(index_df)


if __name__ == "__main__":
    df = pd.read_csv(os.path.join('..', 'week2', 'site_churn_data.csv'))
    df = df.select_dtypes(include=np.number)
    df = df.drop('site_level', axis=1)
    df = pd.DataFrame(SimpleImputer(strategy='mean').fit_transform(df), columns=list(df))
    df = pd.DataFrame(StandardScaler().fit_transform(df), columns=list(df))
    df = df.head(50)
    find_nearest_neighbors(df)
