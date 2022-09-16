import statsmodels.api as sm


# what are ways we can p-hack? (some proven examples for this data are below if needed)
if __name__ == "__main__":
    duncan_prestige = sm.datasets.get_rdataset("Duncan", "carData")
    target = duncan_prestige.data['income']
    predictor = duncan_prestige.data[['education', 'prestige']]
    mod = sm.OLS(target, predictor)
    res = mod.fit()
    print(res.summary())











    # predictor = duncan_prestige.data[['education']]
    # duncan_prestige.data['education'] = np.log(duncan_prestige.data['education'])