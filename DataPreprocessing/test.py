import sys
# tell interpreter where to look
sys.path.insert(0,"..")
from DataScraping.crawler import Crawler
from Preprocess import Data
#Move this to the main function on the process.py
url = 'https://nigerianstat.gov.ng/elibrary'
commodity = 'foodprices'
month_year = 'december 2022'
food_crawler = Crawler(url, commodity, month_year)
data_link = food_crawler.get_data_link(food_crawler.get_page_link())
preprocess_food = Data(data_link, 'SELECTED FOOD AUGUST 2022.xlsx')
df = preprocess_food.create_final_df()
print(df.head())
print(df.shape)
print(df.tail())
# print(len(df.State.unique()))
# print(df.info())


'''
 python Preprocess.py "https://nigerianstat.gov.ng/elibrary" "food" "december" 2022 "SELECTED FOOD DECEMEBER 2022.xlsx" "data.csv"            
 python Preprocess.py "https://nigerianstat.gov.ng/elibrary" "cookinggas" "december" 2022 "GAS PRICE WATCH DECEMBER 2022.xlsx" "gas_data.csv"  
'''                                      