import pandas as pd 
from urllib import request as req
from bs4 import BeautifulSoup as bs
from matplotlib import pyplot as plt
import mplfinance as mpf 
 
#----- install 목록 ---------------------
# pip install beautifulsoup4
# pip install lxml
# pip install pandas
# pip install --upgrade mplfinance
#----------------------------------------


#url = 'https://finance.naver.com/item/sise_day.naver?code=068270&page=1'
url = 'https://finance.naver.com/item/sise_day.nhn?code=068270&page=1'

# 헤더정보 확인
# https://www.whatismybrowser.com/detect/what-is-my-user-agent
headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36')

# User-Agent정보가 없으면 크롤링이 차단됨
opener = req.build_opener()
opener.addheaders = [headers]
response = opener.open(url)
 
#마지막 페이지 구하기 
with opener.open(url) as doc :
    html = bs(response, 'lxml')
    pgrr = html.find('td', class_='pgRR')
    print(pgrr.prettify())

    s = str(pgrr.a['href']).split('=')
    print(s)
    last_page = s[-1]
    print('last page=', last_page)


#전체페이지 읽기
df = pd.DataFrame()
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=068270'

for page in range(1, int(last_page)+1):
    page_url = '{}&page={}'.format(sise_url, page)
    #print(page_url)
    response = opener.open(page_url)
    df = df.append(pd.read_html(response, header=0)[0])

# 데이터 가공 
df = df.dropna()
#print(df)
df = df.iloc[0:30]

# 차트그리기
"""
plt.title('Celltrion (close)')
plt.xticks(rotation=45)
plt.plot(df['날짜'], df['종가'], 'co-')
plt.grid(color='gray', linestyle='--')
plt.show()
"""


# 엠피엘파이낸스로 캔들 차트 그리기
# https://github.com/matplotlib/mplfinance
df = df.rename(columns={'날짜':'Date', '시가':'Open', '고가':'High', '저가':'Low', '종가':'Close', '거래량':'Volume'})
df = df.sort_values(by='Date')
df.index = pd.to_datetime(df.Date)
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

kwargs = dict(title='Celltrion customized chart', type='candle', mav=(2, 4, 6), volume=True, ylabel='ohlc candles')
mc = mpf.make_marketcolors(up='r', down='b', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc)
mpf.plot(df, **kwargs, style=s)
# mpf.plot(df, title='Celltrion candle chart', type='candle')
# mpf.plot(df, title='Celltrion candle chart', type='ohlc')


