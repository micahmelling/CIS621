import os
import numpy as np
import pandas as pd
import warnings

import matplotlib.pyplot as plt
import missingno as msno
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.experimental.enable_iterative_imputer import IterativeImputer


warnings.filterwarnings('ignore')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def visualize_missigness(df, file_name, sample=None):
    if not sample:
        sample = len(df)
    fig = msno.matrix(df.sample(sample))
    fig_copy = fig.get_figure()
    fig_copy.savefig(f'{file_name}.png', bbox_inches='tight')
    plt.clf()


def impute_missing_values(df, strategy, fill_value=None):
    simple_strategies = ['mean', 'median', 'most_frequent', 'constant']
    advanced_strategies = ['linear_model', 'knn_model']
    if strategy in simple_strategies:
        if strategy == 'constant':
            df = pd.DataFrame(SimpleImputer(strategy=strategy, fill_value=fill_value).fit_transform(df), columns=list(df))
        else:
            df = pd.DataFrame(SimpleImputer(strategy=strategy).fit_transform(df), columns=list(df))
    elif strategy == advanced_strategies[0]:
        df = pd.DataFrame(IterativeImputer().fit_transform(df), columns=list(df))
    elif strategy == advanced_strategies[1]:
        df = pd.DataFrame(KNNImputer().fit_transform(df), columns=list(df))
    else:
        raise Exception(f'strategy of {strategy} was passed; it must be one of {advanced_strategies + simple_strategies}')
    return df


if __name__ == "__main__":
    df = pd.read_csv(os.path.join('..', 'week2', 'site_churn_data.csv'))
    df = df.select_dtypes(include=np.number)
    visualize_missigness(df, 'missingness', sample=1_000)
    df = df.drop('site_level', axis=1)
    imputed_df = impute_missing_values(df, strategy='mean')
    print(imputed_df.head(10))
