import sys
from datetime import date, datetime

import click
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

# tell interpreter where to look
sys.path.insert(0, "..")
from DataScraping.crawler import Crawler

# Liquefied Petroleum Gas (Cooking Gas) Price Watch (December 2022)

url = 'https://nigerianstat.gov.ng/elibrary'
commodity = 'cookinggas'
month_year = 'december 2022'

food_crawler = Crawler(url, commodity, month_year)
page_link = food_crawler.get_page_link()
data_link = food_crawler.get_data_link(page_link)
print(page_link)
print(data_link)