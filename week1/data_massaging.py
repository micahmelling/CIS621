import warnings

import numpy as np
import pandas as pd

from week1.ommited_variable_bias import load_data


warnings.filterwarnings('ignore')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def main():
    housing_predictor_df, housing_target = load_data()
    housing_target_df = pd.DataFrame(housing_target, columns=['Price'])
    all_housing_df = pd.merge(housing_predictor_df, housing_target_df, how='inner', left_index=True, right_index=True)
    print(round(all_housing_df.corr()['MedInc']['Price'], 2))

    all_housing_df['MedInc'] = all_housing_df['MedInc'].astype(int)
    all_housing_df['Price'] = all_housing_df['Price'].astype(int)
    print(round(all_housing_df.corr()['MedInc']['Price'], 2))

    all_housing_df['MedInc'] = np.log(all_housing_df['MedInc'])
    all_housing_df['Price'] = np.log(all_housing_df['Price'])
    print(round(all_housing_df.corr()['MedInc']['Price'], 2))

    print(round(all_housing_df.corr()['MedInc']['HouseAge'], 2))
    all_housing_df['MedInc_bin'] = pd.qcut(all_housing_df['MedInc'], q=2, labels=[1, 2])
    all_housing_df['HouseAge_bin'] = pd.qcut(all_housing_df['HouseAge'], q=2, labels=[1, 2])

    cross_tab_df = pd.DataFrame(all_housing_df.groupby(['MedInc_bin', 'HouseAge_bin'])['HouseAge_bin'].count())
    cross_tab_df.columns = ['count']
    cross_tab_df = cross_tab_df.reset_index()
    cross_tab_df['percent'] = cross_tab_df['count'] / len(all_housing_df)
    print(cross_tab_df)


if __name__ == "__main__":
    main()
