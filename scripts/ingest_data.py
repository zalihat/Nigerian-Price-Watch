import urllib.request
from bs4 import BeautifulSoup
import requests
import os
from pathlib import Path
import json
import datetime

class IngestData:
    def get_page_link(self,page_url):
        request = urllib.request.Request(page_url) # The assembled request
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
        
    def get_data_link(self,sub_page_url):

        request=urllib.request.Request(sub_page_url) #The assembled request

        response = urllib.request.urlopen(request)
        soup = BeautifulSoup(response, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            links.append(a['href'])
        links = links[2:]
        links = [link.replace(' ', '%20') for link in links if '.xlsx'  in link.lower()]
        return links    
    def download_and_save_excel(self,url,output_dir):
        """
        Downloads a file from a given URL and saves it with its original filename
        in the 'data/raw/' directory.

        Args:
            url (str): The URL of the file to download.
        """
        raw_data_dir = output_dir
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
            return filename

        except requests.exceptions.RequestException as e:
            print(f"Error downloading file from {url}: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
    def ingest_old_page_data(self, page_url,output_dir, meta_data_file):
        # os.makedirs(meta_data_file, exist_ok=True)  # Create the directory if it doesn't exist
        all_pages_link = self.get_page_link(page_url) # outputs format: [[],[],[],[]]
        all_data_link = []
        for i in all_pages_link:
            all_data_link.extend(self.get_data_link(i[0]))
        print(all_data_link)
        # Load metadata if exists
        METADATA_PATH = Path(meta_data_file) 
        output_dir = Path(output_dir)
        if METADATA_PATH.exists():
            with open(METADATA_PATH, 'r', encoding='utf-8') as f:
                metadata = json.load(f)  
        else:
            metadata = {}
        for link in all_data_link:
            filename = os.path.basename(link)
            local_path = output_dir / filename
            if filename in metadata:
                print(f"[SKIP] {filename} already downloaded.")
                continue
            try:
                self.download_and_save_excel(link, output_dir)
                mod_time = datetime.datetime.fromtimestamp(local_path.stat().st_mtime)
                metadata[filename] = mod_time.isoformat()
                print(f"[DONE] Saved {filename} with last modified {mod_time.isoformat()}")
            except Exception as e:
                print(f"[ERROR] Failed to download {filename}: {e}")
        # === SAVE UPDATED METADATA ===
        with open(METADATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4)

        print("✅ Incremental download complete.")

            # add incremental load strategy here
            
    def get_new_page_links(self,page_url):
        request = urllib.request.Request(page_url) # The assembled request
        try:
            response = urllib.request.urlopen(request)
            soup = BeautifulSoup(response, 'html.parser')
            xlsx_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].lower().endswith('.xlsx')]
            xlsx_links = list(set(xlsx_links))
            print(xlsx_links)
            return xlsx_links
        except urllib.error.URLError as e:
            print(f"Error accessing URL: {e}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
    def ingest_new_page_data(self,page_url,output_dir, meta_data_file):
        all_data_link = self.get_new_page_links(page_url)
        METADATA_PATH = Path(meta_data_file) 
        output_dir = Path(output_dir)
        if METADATA_PATH.exists():
            with open(METADATA_PATH, 'r', encoding='utf-8') as f:
                metadata = json.load(f)  
        else:
            metadata = {}
        for link in all_data_link:
            filename = os.path.basename(link)
            local_path = output_dir / filename
            if filename in metadata:
                print(f"[SKIP] {filename} already downloaded.")
                continue
            try:
                self.download_and_save_excel(link, output_dir)
                mod_time = datetime.datetime.fromtimestamp(local_path.stat().st_mtime)
                metadata[filename] = mod_time.isoformat()
                print(f"[DONE] Saved {filename} with last modified {mod_time.isoformat()}")
            except Exception as e:
                print(f"[ERROR] Failed to download {filename}: {e}")
        # === SAVE UPDATED METADATA ===
        with open(METADATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4)

        print("✅ Incremental download complete.")

        # for i in all_data_link:
        #     self.download_and_save_excel(i, output_dir)
            # add incremental load strategy here
    

        





ingest_data = IngestData()
url = 'https://nigerianstat.gov.ng/elibrary'
# links = ingest_data.get_page_link(url)
# data_links = ingest_data.get_data_link('https://www.nigerianstat.gov.ng/elibrary/read/540')
# print(data_links)
# ingest_data.download_and_save_excel('https://www.nigerianstat.gov.ng/resource/Selected%20food%20price%20watch%20mar%202017-%20proshare.xlsx', 'data/')
METADATA_PATH = Path('data/bronze_metadata.json')
new_page_url = 'https://microdata.nigerianstat.gov.ng/index.php/catalog/162/study-description'
new_page_links = ingest_data.ingest_new_page_data(page_url=new_page_url,output_dir='data/bronze', meta_data_file=METADATA_PATH)
# print(new_page_links)

# ingest_data.ingest_old_page_data(page_url=url, output_dir='data/bronze', meta_data_file=METADATA_PATH)



