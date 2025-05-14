import requests

def download_and_save_excel(url):
    """
    Downloads a file from a given URL and saves it with its original filename.

    Args:
        url (str): The URL of the file to download.
    """
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

        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Successfully downloaded '{filename}'")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file from {url}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage with your provided URL:
download_url = "https://www.nigerianstat.gov.ng/resource/selected_food_oct_2024.xlsx"
download_and_save_excel(download_url)