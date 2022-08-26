import warnings
from bs4 import BeautifulSoup
import pandas as pd
import requests


warnings.filterwarnings('ignore')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

BASE_URL = "http://www.brooksbaseball.net/tabs.php?player=477132&p_hand=1&ppos=1&cn=200&compType=none&gFilt=&time=month&minmax=ci&var=gl&s_type=2&startDate=03/30/2007&endDate=10/22/2016&balls=1&strikes=1&b_hand=1"


def pitch_fx_scraper(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)

    column_headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
    rows = soup.findAll('tr')
    values = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]

    df = pd.DataFrame(values)
    df.columns = column_headers
    df = df.loc[df['Game'] != 'Game']
    df = df.dropna()

    print(df)


if __name__ == "__main__":
    pitch_fx_scraper(
        url=BASE_URL,
    )
