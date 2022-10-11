import sys
# tell interpreter where to look
sys.path.insert(0,"..")
from DataScraping.crawler import Crawler
url = 'https://nigerianstat.gov.ng/elibrary'
commodity = 'food price'
month_year = 'august 2022'
food_crawler = Crawler(url, commodity, month_year)
data_link = food_crawler.get_data_link(food_crawler.get_page_link())
print(data_link)