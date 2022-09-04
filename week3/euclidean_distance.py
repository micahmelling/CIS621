import os
import numpy as np
import pandas as pd
import warnings

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import DistanceMetric


warnings.filterwarnings('ignore')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def find_euclidean_distance(df):
    euc_dist = DistanceMetric.get_metric('euclidean')
    dist_df = pd.DataFrame(euc_dist.pairwise(df))
    print(dist_df.head())


if __name__ == "__main__":
    df = pd.read_csv(os.path.join('..', 'week2', 'site_churn_data.csv'))
    df = df.select_dtypes(include=np.number)
    df = df.drop('site_level', axis=1)
    df = pd.DataFrame(SimpleImputer(strategy='mean').fit_transform(df), columns=list(df))
    df = pd.DataFrame(StandardScaler().fit_transform(df), columns=list(df))
    df = df.head(50)
    find_euclidean_distance(df)
