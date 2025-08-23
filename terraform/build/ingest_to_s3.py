import urllib.request
from bs4 import BeautifulSoup
import requests
import os
from pathlib import Path
import json
import datetime
import boto3

# --------- S3 CONFIG ------------
s3 = boto3.client("s3")
BUCKET_NAME = "nigeria-food-prices0001"  # <-- replace with your Terraform bucket

class IngestData:
    def get_page_link(self, page_url):
        request = urllib.request.Request(page_url)
        try:
            response = urllib.request.urlopen(request)
            soup = BeautifulSoup(response, "html.parser")
            all_links = []
            result = None

            for tr in soup.find_all("tr"):
                rw = tr.find_all("td")
                if rw:
                    row_text_lower = tr.text.replace(" ", "").lower()
                    if "foodprices" in row_text_lower:
                        result = rw
                        links = []
                        for item in result:
                            if item.find("a", href=True):
                                links.append(item.find("a", href=True)["href"])
                        all_links.append(links)

            return all_links

        except urllib.error.URLError as e:
            print(f"Error accessing URL: {e}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def get_data_link(self, sub_page_url):
        request = urllib.request.Request(sub_page_url)
        response = urllib.request.urlopen(request)
        soup = BeautifulSoup(response, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            links.append(a["href"])
        links = links[2:]
        links = [link.replace(" ", "%20") for link in links if ".xlsx" in link.lower()]
        return links

    def download_and_upload_excel(self, url):
        """
        Downloads a file from a given URL and uploads it directly to S3.
        """
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            filename = url.split("/")[-1] or "downloaded_file.xlsx"

            # Upload directly to S3
            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=f"bronze/{filename}",
                Body=response.content,
            )

            print(f"✅ Uploaded '{filename}' to s3://{BUCKET_NAME}/bronze/")
            return filename

        except requests.exceptions.RequestException as e:
            print(f"Error downloading file from {url}: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def load_metadata(self, s3_key="bronze/bronze_metadata.json"):
        try:
            obj = s3.get_object(Bucket=BUCKET_NAME, Key=s3_key)
            return json.loads(obj["Body"].read().decode("utf-8"))
        except s3.exceptions.NoSuchKey:
            return {}
        except Exception as e:
            print(f"⚠️ Could not load metadata: {e}")
            return {}

    def save_metadata(self, metadata, s3_key="bronze/bronze_metadata.json"):
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=json.dumps(metadata, indent=4),
            ContentType="application/json",
        )
        print(f"✅ Metadata updated → s3://{BUCKET_NAME}/{s3_key}")

    def ingest_old_page_data(self, page_url):
        all_pages_link = self.get_page_link(page_url)
        all_data_link = []
        for i in all_pages_link:
            all_data_link.extend(self.get_data_link(i[0]))

        metadata = self.load_metadata()
        for link in all_data_link:
            filename = os.path.basename(link)
            if filename in metadata:
                print(f"[SKIP] {filename} already ingested.")
                continue
            try:
                self.download_and_upload_excel(link)
                metadata[filename] = datetime.datetime.utcnow().isoformat()
                print(f"[DONE] Saved {filename}")
            except Exception as e:
                print(f"[ERROR] Failed to process {filename}: {e}")

        self.save_metadata(metadata)

    def get_new_page_links(self, page_url):
        request = urllib.request.Request(page_url)
        try:
            response = urllib.request.urlopen(request)
            soup = BeautifulSoup(response, "html.parser")
            xlsx_links = [
                a["href"]
                for a in soup.find_all("a", href=True)
                if a["href"].lower().endswith(".xlsx")
            ]
            xlsx_links = list(set(xlsx_links))
            print(xlsx_links)
            return xlsx_links
        except urllib.error.URLError as e:
            print(f"Error accessing URL: {e}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def ingest_new_page_data(self, page_url):
        all_data_link = self.get_new_page_links(page_url)
        metadata = self.load_metadata()

        for link in all_data_link:
            filename = os.path.basename(link)
            if filename in metadata:
                print(f"[SKIP] {filename} already ingested.")
                continue
            try:
                self.download_and_upload_excel(link)
                metadata[filename] = datetime.datetime.utcnow().isoformat()
                print(f"[DONE] Saved {filename}")
            except Exception as e:
                print(f"[ERROR] Failed to process {filename}: {e}")

        self.save_metadata(metadata)


# # ---------- RUN ----------
# ingest_data = IngestData()
# old_page_url = "https://nigerianstat.gov.ng/elibrary"
# new_page_url = "https://microdata.nigerianstat.gov.ng/index.php/catalog/162/study-description"

# # Run either or both
# ingest_data.ingest_old_page_data(old_page_url)
# ingest_data.ingest_new_page_data(new_page_url)

def main():
    ingest_data = IngestData()
    old_page_url = "https://nigerianstat.gov.ng/elibrary"
    new_page_url = "https://microdata.nigerianstat.gov.ng/index.php/catalog/162/study-description"

    print("🚀 Starting ingestion pipeline...")

    print("\n--- Ingesting OLD PAGE data ---")
    ingest_data.ingest_old_page_data(old_page_url)

    print("\n--- Ingesting NEW PAGE data ---")
    ingest_data.ingest_new_page_data(new_page_url)

    print("\n✅ All ingestion tasks complete.")


if __name__ == "__main__":
    main()

