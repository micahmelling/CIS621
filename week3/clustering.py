from copy import deepcopy
import operator
import os

import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


np.random.seed(200)


def run_kmeans_clustering(df, drop_list, max_clusters, fill_na_value=0, samples=25_000):
    """
    Runs a k-means clustering algorithm to assign each observation to a cluster.

    :param df: pandas dataframe we want to run the clustering algorithm on
    :param drop_list: features we want to exclude from clustering
    :param max_clusters: the maximum number of clusters to potentially have
    :param fill_na_value: value to fill for missing numeric values
    :param samples: Since k-means can be computationally expensive, we might want to only run it on a subset of data
    :returns: pandas dataframe that can be used in get_cluster_summary()
    """
    print('running k-means clustering...')
    append_df = deepcopy(df)
    append_df = append_df.sample(n=samples)
    append_df = pd.get_dummies(append_df, dummy_na=True)
    append_df.fillna(value=fill_na_value, inplace=True)
    cluster_df = append_df.drop(drop_list, 1)
    cluster_df = pd.DataFrame(StandardScaler().fit_transform(cluster_df), columns=list(cluster_df))
    silhouette_dict = {}
    n_clusters = list(np.arange(2, max_clusters + 1, 1))
    for n in tqdm(n_clusters):
        kmeans = KMeans(n_clusters=n, random_state=19)
        labels = kmeans.fit_predict(cluster_df)
        silhouette_mean = silhouette_score(cluster_df, labels)
        silhouette_dict[n] = silhouette_mean
    best_n = max(silhouette_dict.items(), key=operator.itemgetter(1))[0]
    kmeans = KMeans(n_clusters=best_n, random_state=19)
    labels = kmeans.fit_predict(cluster_df)
    append_df['cluster'] = labels
    return append_df


def get_cluster_summary(df, cluster_column_name):
    """
    Produces a summary of the cluster results and saves it locally.
    :param df: pandas dataframe produced by run_kmeans_clustering()
    :param cluster_column_name: name of the column that identifies the cluster label
    :param save_path: path in which to save the output
    """
    mean_df = df.groupby(cluster_column_name).mean().reset_index()
    sum_df = df.groupby(cluster_column_name).sum().reset_index()
    count_df = df.groupby(cluster_column_name).count().reset_index()
    mean_df = pd.melt(mean_df, id_vars=[cluster_column_name])
    mean_df.rename(columns={'value': 'mean'}, inplace=True)
    sum_df = pd.melt(sum_df, id_vars=[cluster_column_name])
    sum_df.rename(columns={'value': 'sum'}, inplace=True)
    count_df = pd.melt(count_df, id_vars=[cluster_column_name])
    count_df.rename(columns={'value': 'count'}, inplace=True)
    summary_df = pd.merge(mean_df, sum_df, how='inner', on=['cluster', 'variable'])
    summary_df = pd.merge(summary_df, count_df, how='inner', on=['cluster', 'variable'])
    summary_df.to_csv(os.path.join('cluster_summary.csv'), index=False)


if __name__ == "__main__":
    df = pd.read_csv(os.path.join('..', 'week2', 'site_churn_data.csv'))
    df['churn'] = np.where(df['churn'].str.startswith('y'), 1, 0)
    df = df.select_dtypes(include=np.number)
    df = df.drop('site_level', axis=1)
    df = pd.DataFrame(SimpleImputer(strategy='mean').fit_transform(df), columns=list(df))
    df = pd.DataFrame(StandardScaler().fit_transform(df), columns=list(df))
    cluster_df = run_kmeans_clustering(df, ['churn'], max_clusters=5, samples=10_000)
    get_cluster_summary(cluster_df, 'cluster')
