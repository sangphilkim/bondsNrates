# Import Libraries
import pandas as pd
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('headless')

# Access WSJ Pages
driver = webdriver.Chrome('/Users/sangphilkim/Chromedriver', options=options)
driver.get("https://www.wsj.com/market-data/bonds")

# Get Treasury Table
path = '//*[@id="root"]/div/div/div/div[2]/div[4]/div[1]/div[2]/div[1]/div'
table = driver.find_element_by_xpath(path)

# Convert Data to DataFrame
rows = table.text.split('\n')
element = []
for r in rows:
    element.append([i for i in r.split(' ')])
df = pd.DataFrame(element)
headers = ['Maturity', 'Type', 'Coupon', 'Price Chg', 'Yield', 'Yield Chg']
df.columns = headers
df.iloc[:] = df.iloc[::-1].values

print(df)