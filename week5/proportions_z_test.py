# https://www.statsmodels.org/devel/generated/statsmodels.stats.proportion.proportions_ztest.html

import numpy as np
from statsmodels.stats.proportion import proportions_ztest


# if the p-value <= our cutoff of 0.05, we can reject the null and determine the *proportions are different*
# if the p-value is > our cutoff of 0.05, we cannot reject the null; we determine the *proportions are the same*


# example take straight from the documentation
def main():
    # null hypothesis: both have the same rates
    count = np.array([5, 25])
    nobs = np.array([83, 99])
    stat, pval = proportions_ztest(count, nobs)
    print('{0:0.3f}'.format(pval))


if __name__ == "__main__":
    main()
