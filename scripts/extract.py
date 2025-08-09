import urllib.request
from bs4 import BeautifulSoup
import requests
import os
def get_page_link():
  url = 'https://nigerianstat.gov.ng/elibrary'
  request = urllib.request.Request(url) # The assembled request
  try:
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response, 'html.parser')
    all_links = []
    result = None  # Initialize result outside the loop

    for tr in soup.find_all('tr'):
      rw = tr.find_all('td')
      if rw:  # Ensure there are 'td' elements in the row
        row_text_lower = tr.text.replace(' ', '').lower()
        if 'foodprices' in row_text_lower:
          result = rw
          links = []
          for item in result:
            if item.find('a', href=True):
              links.append(item.find('a', href=True)['href'])
          all_links.append(links)

    return all_links

  except urllib.error.URLError as e:
    print(f"Error accessing URL: {e}")
    return []
  except Exception as e:
    print(f"An error occurred: {e}")
    return []
# print(get_page_link())

def get_data_link(url):
  # url = get_page_link('877')[0][0]

  request=urllib.request.Request(url) #The assembled request

  response = urllib.request.urlopen(request)
  soup = BeautifulSoup(response, 'html.parser')
  links = []
  for a in soup.find_all('a', href=True):
      links.append(a['href'])
  links = links[2:]
  links = [link.replace(' ', '%20') for link in links if '.xlsx'  in link.lower()]
  return links
def download_and_save_excel(url):
    """
    Downloads a file from a given URL and saves it with its original filename
    in the 'data/raw/' directory.

    Args:
        url (str): The URL of the file to download.
    """
    raw_data_dir = 'data/bronze/'
    os.makedirs(raw_data_dir, exist_ok=True)  # Create the directory if it doesn't exist

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Extract the filename from the Content-Disposition header if available
        content_disposition = response.headers.get("Content-Disposition")
        if content_disposition:
            filename = content_disposition.split("filename=")[-1].strip('"')
        else:
            # If no Content-Disposition header, try to extract from the URL
            filename = url.split("/")[-1]

        if not filename:
            filename = "downloaded_file.xlsx" # Default if no filename found

        filepath = os.path.join(raw_data_dir, filename)

        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Successfully downloaded '{filename}' to '{raw_data_dir}'")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file from {url}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

all_pages_link = get_page_link() # outputs format: [[],[],[],[]]
all_data_link = []
for i in all_pages_link:
  # print(i[0])
  all_data_link.extend(get_data_link(i[0]))
print(all_data_link)
for i in all_data_link:
  download_and_save_excel(i)
  
