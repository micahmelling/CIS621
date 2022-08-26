import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def load_data():
    """
    https://inria.github.io/scikit-learn-mooc/python_scripts/datasets_california_housing.html
    """
    data_bunch = fetch_california_housing()
    target = data_bunch.target
    predictors = pd.DataFrame(data_bunch.data, columns=data_bunch.feature_names)
    predictors = predictors.drop(labels=['Latitude', 'Longitude'], axis=1)
    return predictors, target


def make_train_test_split(x, y, test_size=0.25):
    return train_test_split(x, y, test_size=test_size, random_state=42)


def fit_linear_regression(x_train, y_train):
    model = LinearRegression()
    model.fit(x_train, y_train)
    return model


def extract_feature_names(x_train):
    return list(x_train)


def extract_model_coefs(model):
    return model.coef_


def make_coef_df(coefs, features):
    return pd.DataFrame({
        'feature': features,
        'coef': coefs
    })


def drop_features(df, features_to_drop):
    return df.drop(labels=features_to_drop, axis=1)


def compare_model_coefs(coef_df1, coef_df2):
    coef_df1 = coef_df1.rename(columns={'coef': 'coef_model_1'})
    coef_df2 = coef_df2.rename(columns={'coef': 'coef_model_2'})
    merged_df = pd.merge(coef_df1, coef_df2, how='left', on='feature')
    return merged_df


def train_linear_regression_and_produce_coefs(x_train, y_train):
    model = fit_linear_regression(x_train, y_train)
    feature_names = extract_feature_names(x_train)
    model_coefs = extract_model_coefs(model)
    coef_df = make_coef_df(model_coefs, feature_names)
    return coef_df


def main(features_to_drop):
    housing_predictor_df, housing_target = load_data()
    x_train, x_test, y_train, y_test = make_train_test_split(housing_predictor_df, housing_target)
    original_coef_df = train_linear_regression_and_produce_coefs(x_train, y_train)

    x_train = drop_features(x_train, features_to_drop)
    updated_coef_df = train_linear_regression_and_produce_coefs(x_train, y_train)
    coef_comparison_df = compare_model_coefs(original_coef_df, updated_coef_df)
    print(coef_comparison_df)


if __name__ == "__main__":
    main(
        features_to_drop=['AveBedrms']
    )
