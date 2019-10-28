import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup

tenors = ['01M', '03M', '06M', '01Y', '02Y', '03Y', '05Y', '07Y', '10Y', '30Y']

maturities =[]
yields = []
coupons = []

for tenor in tenors:
    req = requests.get("https://quotes.wsj.com/bond/BX/TMUBMUSD" + tenor + "?mod=md_bond_overview_quote")

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    data1 = soup.select('body > div > div > section > div > div > div > ul > li > span > span')
    data2 = soup.select('body > div > div > section > div > div > div > ul > li > div > span')

    ytm = data1[0].text
    coupon = data2[6].text
    maturity = data2[8].text

    ytm = float(ytm[:-1])
    if coupon != '':
        coupon = float(coupon[:-1])
    else:
        coupon = 0.0
    maturity = datetime.datetime.strptime(maturity, '%m/%d/%y').date()

    yields.append(ytm)
    coupons.append(coupon)
    maturities.append(maturity)

df = pd.DataFrame([maturities, yields, coupons]).transpose()
headers = ['maturity', 'yield', 'coupon']
df.columns = headers
df.set_index('maturity', inplace=True)

print(df)
