import matplotlib.pyplot as plt
import pandas as pd

from copy import deepcopy


def generate_data():
    df = pd.DataFrame({
        'payment_method': [
            'card', 'card', 'card', 'card',
            'check', 'check', 'check', 'check',
            'debit_card', 'debit_card', 'debit_card', 'debit_card',
            'credit_card', 'credit_card', 'credit_card', 'credit_card',
        ],
        'volume': [
            1_010, 989, 1215, 0,
            567, 613, 633, 591,
            0, 0, 0, 554,
            0, 0, 0, 607,
        ],
        'month': [
            '2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01',
            '2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01',
            '2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01',
            '2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01',
        ]
    })
    return df


def plot_multiple_lines(df, x_col, y_col, label_col, file_name, plot_title):
    df_copy = deepcopy(df)
    labels = list(df[label_col].unique())
    for label in labels:
        label_df = df_copy.loc[df_copy[label_col] == label]
        plt.plot(label_df[x_col], label_df[y_col], label=label)
        plt.legend()
    plt.title(plot_title)
    plt.savefig(f'{file_name}.png')
    plt.clf()


def main():
    transactions_df = generate_data()
    plot_multiple_lines(transactions_df, 'month', 'volume', 'payment_method', 'transactions_ts',
                        'Monthly Transaction Volume')


if __name__ == "__main__":
    main()

