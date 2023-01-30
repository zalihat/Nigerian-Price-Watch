import sys
# tell interpreter where to look
sys.path.insert(0,"..")
from DataScraping.crawler import Crawler
from Preprocess import Data
url = 'https://nigerianstat.gov.ng/elibrary'
commodity = 'food price'
month_year = 'september 2022'
path = "../DataPreprocessing/SELECTED FOOD AUGUST 2022.xlsx"
food_crawler = Crawler(url, commodity, month_year)
# data_link = food_crawler.get_data_link(food_crawler.get_page_link())
preprocess_food = Data(url, commodity, month_year, path)
df = preprocess_food.create_final_df()
print(df.head())
print(df.shape)
print(df.tail())
print(len(df.State.unique()))
print(df.info())