from bs4 import BeautifulSoup
import requests
import urllib.request 
import logging
import warnings
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO)

class Crawler:
    def __init__(self, url, month_year):
        url = self.url
        month_year = self.month_year
    def get_page_link(self, month_year):
        # url = 'https://nigerianstat.gov.ng/elibrary'
        request=urllib.request.Request(self.url,) #The assembled request
        response = urllib.request.urlopen(request)
        soup = BeautifulSoup(response, 'html.parser')
        for tr in soup.find_all('tr'):
            rw = tr.findAll('td')
            if 'food prices' in tr.text.lower() and month_year in tr.text.lower():
            result = rw
        links = []
        for a in result[-1].find_all('a', href=True):
            links.append(a['href'])
        return links[0]
    
    def get_data_link(link_to_page):
        request=urllib.request.Request(link_to_page,) #The assembled request
        response = urllib.request.urlopen(request)
        soup = BeautifulSoup(response, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            links.append(a['href'])
        links = links[2:]
        links = [link.replace(' ', '%20') for link in links if '.xlsx'  in link.lower()]
        return links[0]
