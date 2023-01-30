import sys
sys.path.insert(0,"..")
from DataScraping.crawler import Crawler
from DataPreprocessing.Preprocess import Data 
url = 'https://nigerianstat.gov.ng/elibrary'
commodity = 'food price'
month_year = 'october 2022'
path = "../DataPreprocessing/SELECTED FOOD AUGUST 2022.xlsx"
# food_crawler = Crawler(url, commodity, month_year)
# data_link = food_crawler.get_data_link(food_crawler.get_page_link())
preprocess_food = Data(url, commodity, month_year, path)
df = preprocess_food.create_final_df()
print(df.tail())
df.to_csv('Processed_data.csv')