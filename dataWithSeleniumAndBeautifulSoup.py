import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('headless')

##page contact using Chromedriver
driver = webdriver.Chrome('/Users/sangphilkim/Chromedriver/chromedriver', options=options)
driver.get("https://www.wsj.com/market-data/bonds/treasuries")

source = driver.page_source
tbonds_code = BeautifulSoup(source, 'html.parser')

##acquire treasury bills data
button_xpath = '//*[@id="root"]/div/div/div/div[2]/div/div/div[3]/ul/li[2]/button'
button = driver.find_element_by_xpath(button_xpath)
button.click()

source = driver.page_source
tbills_code = BeautifulSoup(source, 'html.parser')

##select data what you need
date = tbonds_code.select('div > div > div > div > div > div > div > div > h3 > span')
date = date[1].text
tbond_rows = tbonds_code.select('div > div > div > div > div > div > div > div > table > tbody > tr')
tbill_rows = tbills_code.select('div > div > div > div > div > div > div > div > table > tbody > tr')

##set dataframe for bond
tbond_content = []
tbond_contents = []

for tbond_row in tbond_rows:
    tds = tbond_row.find_all("td")
    for td in tds:
        tbond_content.append(td.text)
    tbond_contents.append(tbond_content)
    tbond_content = []

tbond_df = pd.DataFrame(tbond_contents)
tbond_headers = ['Maturity', 'Coupon', 'Bid', 'Ask', 'Chg', 'Asked Yield']
tbond_df.columns = tbond_headers
tbond_df.set_index('Maturity', inplace=True)

##set dataframe for bill
tbill_content = []
tbill_contents = []

for tbill_row in tbill_rows:
    tds = tbill_row.find_all("td")
    for td in tds:
        tbill_content.append(td.text)
    tbill_contents.append(tbill_content)
    tbill_content = []

tbill_df = pd.DataFrame(tbill_contents)
tbill_headers = ['Maturity', 'Bid', 'Ask', 'Chg', 'Asked Yield']
tbill_df.columns = tbill_headers
tbill_df.set_index('Maturity', inplace=True)

##print
print(tbond_df.head())
print(tbill_df.head())

