import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import QuantLib as ql

options = webdriver.ChromeOptions()
options.add_argument('headless')


def GET_DATE():
    driver = webdriver.Chrome('C:\chromedriver', options=options)
    driver.get("https://www.wsj.com/market-data/bonds")
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find("span", class_="WSJBase--card__timestamp--2xDXNOQk")
    date = data.text
    date = date.split(' ')[3]
    date = datetime.datetime.strptime(date, "%m/%d/%y").date()
    return date


def GET_QUOTE(reference_date):
    driver = webdriver.Chrome('C:\chromedriver', options=options)
    tenors = ['01M', '03M', '06M', '01Y', '02Y', '03Y', '05Y', '07Y', '10Y', '30Y']

    # Create Empty Lists
    maturities = []
    days = []
    prices = []
    coupons = []

    # Get Market Information
    for i, tenor in enumerate(tenors):
        driver.get("https://quotes.wsj.com/bond/BX/TMUBMUSD" + tenor + "?mod=md_bond_overview_quote")
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Price
        if i <= 3:
            data_src = soup.find("span", id="quote_val")
            price = data_src.text
            price = float(price[:-1])
        else:
            data_src = soup.find("span", id="price_quote_val")
            price = data_src.text
            price = price.split()
            price1 = float(price[0])
            price = price[1].split('/')
            price2 = float(price[0])
            price3 = float(price[1])
            price = price1 + (price2 / price3)

        data_src2 = soup.find_all("span", class_="data_data")

        # Coupon
        coupon = data_src2[2].text
        if coupon != '':
            coupon = float(coupon[:-1])
        else:
            coupon = 0.0

        # Maturity Date
        maturity = data_src2[3].text
        maturity = datetime.datetime.strptime(maturity, '%m/%d/%y').date()

        # Send to Lists
        days.append((maturity - reference_date).days)
        prices.append(price)
        coupons.append(coupon)
        maturities.append(maturity)

    # Create DataFrame
    df = pd.DataFrame([maturities, days, prices, coupons]).transpose()
    headers = ['maturity', 'days', 'price', 'coupon']
    df.columns = headers
    df.set_index('maturity', inplace=True)

    return df


def TREASURY_CURVE(date, quote):
    # Divide Quotes
    tbill = quote[0:4]
    tbond = quote[4:]

    # Set Evaluation Date
    eval_date = ql.Date(date.day, date.month, date.year)
    ql.Settings.instance().evaluationDate = eval_date

    # Set Market Conventions
    calendar = ql.UnitedStates()
    convention = ql.ModifiedFollowing
    day_counter = ql.ActualActual()
    end_of_month = False
    fixing_days = 1
    face_amount = 100
    coupon_frequency = ql.Period(ql.Semiannual)

    # Construct Treasury Bill Helpers
    bill_helpers = [ql.DepositRateHelper(ql.QuoteHandle(ql.SimpleQuote(r / 100.0)),
                                         ql.Period(m, ql.Days),
                                         fixing_days,
                                         calendar,
                                         convention,
                                         end_of_month,
                                         day_counter)
                    for r, m in zip(tbill['price'], tbill['days'])]

    # Construct Treasury Bond Helpers
    bond_helpers = []
    for p, c, m in zip(tbond['price'], tbond['coupon'], tbond['days']):
        termination_date = eval_date + ql.Period(m, ql.Days)
        schedule = ql.Schedule(eval_date,
                               termination_date,
                               coupon_frequency,
                               calendar,
                               convention,
                               convention,
                               ql.DateGeneration.Backward,
                               end_of_month)
        bond_helper = ql.FixedRateBondHelper(ql.QuoteHandle(ql.SimpleQuote(p)),
                                             fixing_days,
                                             face_amount,
                                             schedule,
                                             [c / 100.0],
                                             day_counter,
                                             convention)
        bond_helpers.append(bond_helper)

    # Bind Helpers
    rate_helper = bill_helpers + bond_helpers

    # Build Curve
    yc_linearzero = ql.PiecewiseLinearZero(eval_date, rate_helper, day_counter)

    return yc_linearzero


def DISCOUNT_FACTOR(date, curve):
    date = ql.Date(date.day, date.month, date.year)
    return curve.discount(date)


def ZERO_RATE(date, curve):
    date = ql.Date(date.day, date.month, date.year)
    day_counter = ql.ActualActual()
    compounding = ql.Compounded
    freq = ql.Continuous
    zero_rate = curve.zeroRate(date, day_counter, compounding, freq).rate()
    return zero_rate


if __name__ == "__main__":
    ref_date = GET_DATE()
    quote = GET_QUOTE(ref_date)
    curve = TREASURY_CURVE(ref_date, quote)

    quote['discount factor'] = np.nan
    quote['zero rate'] = np.nan

    for date in quote.index:
        quote.loc[date, 'discount factor'] = DISCOUNT_FACTOR(date, curve)
        quote.loc[date, 'zero rate'] = ZERO_RATE(date, curve)

    print(quote[['discount factor', 'zero rate']])

    plt.figure(figsize=(16, 8))
    plt.plot(quote['zero rate'], 'b.-')
    plt.title('Zero Curve', loc='center')
    plt.xlabel('Maturity')
    plt.ylabel('Zero Rate')

    plt.figure(figsize=(16, 8))
    plt.plot(quote['discount factor'], 'r.-')
    plt.title('Discount Curve', loc='center')
    plt.xlabel('Maturity')
    plt.ylabel('Discount Factor')