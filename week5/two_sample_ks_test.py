import os

import pandas as pd
from scipy.stats import ks_2samp

from ks_test import make_density_plot

# If the p-value is lower than our threshold of 0.05, the data are from different distributions.
# If the p-value is greater than our threshold of 0.05, the data are from the same distributions.


def calculate_ks_statistic(training_df, production_df, feature):
    try:
        ks_result = ks_2samp(training_df[feature], production_df[feature])
        return ks_result[1]
    except KeyError:
        return 0.00


if __name__ == "__main__":
    df = pd.read_csv(os.path.join('..', 'week2', 'site_churn_data.csv'))

    df = df[['activity_score', 'acquired_date']]
    df['acquired_date'] = pd.to_datetime(df['acquired_date'])
    df = df.loc[df['acquired_date'] >= '2019-01-01']

    train_df = df.loc[df['acquired_date'] <= '2019-06-30']
    prod_df = df.loc[df['acquired_date'] >= '2019-07-01']
    # make_density_plot(train_df['activity_score'], save=True, file_name='train')
    # make_density_plot(prod_df['activity_score'], save=True, file_name='prod')

    p_value = calculate_ks_statistic(train_df, prod_df, 'activity_score')
    print(p_value)
