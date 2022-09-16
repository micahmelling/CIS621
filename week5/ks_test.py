import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import kstest, norm
from sklearn.preprocessing import PowerTransformer


# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kstest.html
# Statements taken directed from the documentation
# "Indeed, the p-value is lower than our threshold of 0.05, so we reject the null hypothesis in favor of the default
# “two-sided” alternative: the data are not distributed according to the standard normal."
# "As expected, the p-value of 0.92 is not below our threshold of 0.05, so we cannot reject the null hypothesis."

# If the p-value is lower than our threshold of 0.05, the data are from different distributions.
# If the p-value is greater than our threshold of 0.05, the data are from the same distributions.


def generate_series(df, column):
    srs = df[column]
    srs = srs.dropna()
    return srs


def make_density_plot(series, save=None, file_name=None):
    sns.kdeplot(data=series)
    if save:
        plt.savefig(f'{file_name}.png')
        plt.clf()
    else:
        plt.show()


def apply_power_transform(df):
    df = df.select_dtypes(include=np.number)
    return pd.DataFrame(PowerTransformer(method='box-cox').fit_transform(df), columns=list(df))


def run_one_sample_norm_ks_test(series):
    # null hypothesis: the two distributions are the same
    results = kstest(series, norm.cdf)
    print(results)


if __name__ == "__main__":
    iris_df = sns.load_dataset("iris")
    column = 'sepal_length'
    srs = generate_series(iris_df, column)
    # make_density_plot(srs)
    run_one_sample_norm_ks_test(srs)

    transformed_df = apply_power_transform(iris_df)
    transformed_srs = transformed_df[column]
    # make_density_plot(transformed_srs)
    run_one_sample_norm_ks_test(transformed_srs)
