# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.anderson.html
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.anderson_ksamp.html

import os

import pandas as pd
from scipy.stats import anderson
from numpy import random

from ks_test import make_density_plot, run_one_sample_norm_ks_test

# From the documentation linked above
# "If the returned statistic is larger than these critical values, then for the corresponding significance level,
# the null hypothesis that the data come from the chosen distribution can be rejected."

# In other words, if the returned statistic is larger than the critical value of choice, then the distributions
# are different.
# if the returned statistic is lower than the critical value of choice, then the distributions are the same.


def generate_series(column):
    df = pd.read_csv(os.path.join('..', 'week2', 'site_churn_data.csv'))
    srs = df[column]
    return srs


def run_anderson_test(srs, comparison_dist='norm'):
    # null hypothesis: data come from the same distribution
    results = anderson(srs, dist=comparison_dist)
    print(results)


if __name__ == "__main__":
    # e = random.exponential(scale=1.0, size=1_000)
    # run_anderson_test(e)
    # n = random.normal(loc=0.0, scale=1.0, size=1_000)
    # run_anderson_test(n)

    column = 'activity_score'
    srs = generate_series(column)
    srs = srs.dropna()
    print(srs.mean())
    print(srs.std())
    # make_density_plot(srs)
    run_anderson_test(srs)
    run_one_sample_norm_ks_test(srs)

