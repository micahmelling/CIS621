import os

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_selector as selector
from sklearn.impute import SimpleImputer


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def _find_non_dummied_columns(df):
    cols = list(df)
    non_dummied_cols = []
    for col in cols:
        unique_col_vals = list(df[col].unique())
        if set(unique_col_vals) not in [{0, 1}, {0}, {1}]:
            non_dummied_cols.append(col)
    return non_dummied_cols


def load_and_clean_data():
    df = pd.read_csv(os.path.join('..', 'week2', 'site_churn_data.csv'))
    df = df.drop(['site_level', 'client_id', 'acquired_date'], axis=1)
    df['churn'] = np.where(df['churn'].str.startswith('y'), 'yes', 'no')
    return df


def impute_missing_values(df):
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
    ])
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='unknown')),
    ])
    preprocessor = ColumnTransformer(
        transformers=[
            ('numeric_transformer', numeric_transformer, selector(dtype_include='number')),
            ('categorical_transformer', categorical_transformer, selector(dtype_exclude='number'))
        ],
        remainder='passthrough',
    )
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
    ])

    column_names = list(df)
    df = pd.DataFrame(pipeline.fit_transform(df))
    df.columns = column_names
    return df


def convert_to_float_if_possible(df):
    for column in list(df):
        try:
            df[column] = df[column].astype(float)
        except:
            pass
    return df


def dummy_code(df):
    return pd.get_dummies(df)


def get_feature_summary(df):
    non_dummed_columns = _find_non_dummied_columns(df)
    columns = list(df)

    summary_stats_df = pd.DataFrame()
    for column in columns:
        if column in non_dummed_columns:
            col_value = df[column].median()
            metric = 'median'
        else:
            col_value = df[column].mean()
            metric = 'percentage'
        col_df = pd.DataFrame({
            'column': [column],
            'value': [col_value],
            'metric': [metric]
        })
        summary_stats_df = summary_stats_df.append(col_df)

    return summary_stats_df


def produce_summary_comparison(overall_summary_df, sample_summary_df):
    sample_comparison_df = pd.merge(overall_summary_df, sample_summary_df, how='inner', on='column')
    sample_comparison_df['diff'] = sample_comparison_df['value_x'] - sample_comparison_df['value_y']
    sample_comparison_df['diff'] = sample_comparison_df['diff'].abs()
    sample_comparison_df = sample_comparison_df.sort_values(by=['diff'], ascending=False)
    return sample_comparison_df


if __name__ == "__main__":
    site_df = load_and_clean_data()
    site_df = impute_missing_values(site_df)
    site_df = convert_to_float_if_possible(site_df)
    site_df = dummy_code(site_df)
    overall_feature_summary_df = get_feature_summary(site_df)

    sample_100_df = site_df.sample(n=100)
    sample_100_summary_df = get_feature_summary(sample_100_df)
    comparison_df = produce_summary_comparison(overall_feature_summary_df, sample_100_summary_df)
    print(comparison_df)
