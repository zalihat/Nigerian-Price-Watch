from bs4 import BeautifulSoup
import requests
import urllib.request
import logging
import warnings
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO)

class Crawler:
  def __init__(self, url, commodity, month_year):
    self.url = url
    self.month_year = month_year
    self.commodity = commodity
  def get_page_link(self):
    #
    request=urllib.request.Request(self.url,) #The assembled request
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response, 'html.parser')
    for tr in soup.find_all('tr'):
      rw = tr.findAll('td')
    #   print(
      if self.commodity in tr.text.lower() and self.month_year in tr.text.lower():
        result = rw
    links = []
    for a in result[-1].find_all('a', href=True):
      links.append(a['href'])
    # print(links)
    return links[0]

  def get_data_link(self, link_to_page):

    request=urllib.request.Request(link_to_page,) #The assembled request
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True):
      links.append(a['href'])
    links = links[2:]
    links = [link.replace(' ', '%20') for link in links if '.xlsx'  in link.lower()]
    return links[0]
url = 'https://nigerianstat.gov.ng/elibrary'
food_crawler = Crawler(url, 'food price', 'october 2024')
data_link = food_crawler.get_data_link(food_crawler.get_page_link())
print(food_crawler.get_page_link())
print(data_link)