import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE


def create_tsne_visualization(df, target, save_path, sample_size=10_000):
    """
    Creates a t-SNE visualization and saves it into IMAGES_PATH. The visualization will help us visualize our entire
    dataset and will highlight the data points in each class. This will allow us to see how clustered or interspersed
    our target classes are.

    :param df: pandas dataframe
    :param target: name of the target
    :param sample_size: number of observations to sample since t-SNE is computationally expensive; default is 10_000
    :param save_path: path in which to save the output
    """
    print('creating tsne visualization...')
    df = df.sample(n=sample_size)
    target_df = df[[target]]
    df = df.drop(target, 1)
    df = df.select_dtypes(include=['float64', 'float32', 'int'])
    df.dropna(how='all', inplace=True, axis=1)
    df = pd.DataFrame(SimpleImputer(strategy='mean', copy=False).fit_transform(df), columns=list(df))
    df = pd.DataFrame(StandardScaler().fit_transform(df), columns=list(df))

    tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
    tsne_results = tsne.fit_transform(df)
    target_df['tsne_2d_one'] = tsne_results[:, 0]
    target_df['tsne_2d_two'] = tsne_results[:, 1]

    plt.figure(figsize=(16, 10))
    sns.scatterplot(
        x="tsne_2d_one",
        y="tsne_2d_two",
        palette=sns.color_palette("hls", 2),
        data=target_df,
        hue=target,
        legend="full",
        alpha=0.3
    )
    plt.title('TSNE Plot')
    plt.savefig(save_path)
    plt.clf()


if __name__ == "__main__":
    df = pd.read_csv(os.path.join('..', 'week2', 'site_churn_data.csv'))
    df['churn'] = np.where(df['churn'].str.contains('y'), 'yes', 'no')
    create_tsne_visualization(
        df=df,
        target='churn',
        save_path='tsne.png'
    )
