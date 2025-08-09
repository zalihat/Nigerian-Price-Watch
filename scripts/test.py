# # from pathlib import Path
# # import datetime
# # # data\bronze\PRICES_OF_SELECTED_FOOD_ITEMS_(JAN%20%202018).xlsx
# # file_path = Path('data/bronze/PRICES_OF_SELECTED_FOOD_ITEMS_(JAN%20%202018).xlsx')

# # mod_time = file_path.stat().st_mtime
# # mod_datetime = datetime.datetime.fromtimestamp(mod_time)

# # print(f"Last modified: {mod_datetime}")

# import os
# import json
# import requests
# from pathlib import Path
# from bs4 import BeautifulSoup
# import datetime

# # === CONFIGURATION ===
# BASE_URL = 'https://example.com/page-with-xlsx-links'  # 🔁 Replace with actual URL
# DOWNLOAD_DIR = Path('data/bronze')
# METADATA_PATH = Path('data/bronze_metadata.json')

# # === SETUP ===
# DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

# # Load metadata if exists
# if METADATA_PATH.exists():
#     with open(METADATA_PATH, 'r', encoding='utf-8') as f:
#         metadata = json.load(f)
# else:
#     metadata = {}

# # === GET .xlsx LINKS FROM PAGE ===
# html = requests.get(BASE_URL).text
# soup = BeautifulSoup(html, 'html.parser')

# xlsx_links = [
#     a['href'] for a in soup.find_all('a', href=True)
#     if a['href'].lower().endswith('.xlsx')
# ]

# # === DOWNLOAD FILES INCREMENTALLY ===
# for link in xlsx_links:
#     filename = os.path.basename(link)
#     local_path = DOWNLOAD_DIR / filename

#     if filename in metadata:
#         print(f"[SKIP] {filename} already downloaded.")
#         continue

#     try:
#         print(f"[DOWNLOAD] {filename}...")
#         response = requests.get(link)
#         response.raise_for_status()

#         with open(local_path, 'wb') as f:
#             f.write(response.content)

#         # Get last modified time of the file on disk
#         mod_time = datetime.datetime.fromtimestamp(local_path.stat().st_mtime)
#         metadata[filename] = mod_time.isoformat()

#         print(f"[DONE] Saved {filename} with last modified {mod_time.isoformat()}")

#     except Exception as e:
#         print(f"[ERROR] Failed to download {filename}: {e}")

# # === SAVE UPDATED METADATA ===
# with open(METADATA_PATH, 'w', encoding='utf-8') as f:
#     json.dump(metadata, f, indent=4)

# print("✅ Incremental download complete.")
ColumnMap = {
    "agric_eggs": [
        "Agric eggs medium size",
        # "Agric eggs(medium size price of one)",
        # "Agric hen eggs, ",
        "Agric hen eggs, (a Crate of 30 pieces)",
    ],
    "agric eggs(medium size price of one)": [
        "Agric eggs(medium size price of one)",
        "Agric hen eggs, "

    ],
    "beans_brown": [
        "Beans Brown",
        "Beans brown,sold loose"

    ],
    # "beans_brown": [
    #     "Beans Brown",
    #     "Beans brown,sold loose"
    # ],
    # "beans_white": [
    #     "Beans white"
    # ],
    "beans_blackeye": [
        "Beans:white black eye. sold loose",
        "Beans white"
    ],
    "beef_bone_in": [
        "Beef Bone in"
    ],
    "beef_boneless": [
        "Beef Boneless",
        "Beef,boneless"
    ],
    "bread_sliced": [
        "Bread (sliced), 450g",
        "Bread sliced 500g"
    ],
    "bread_unsliced": [
        "Bread (unsliced), 450g",
        "Bread unsliced 500g"
    ],
    "rice_ofada": [
        "Broken Rice (Ofada)"
    ],
    "carrots_fresh": [
        "Carrots, fresh"
    ],
    "catfish_fresh": [
        "Cat fresh fish",
        "Catfish (obokun) fresh"
    ],
    "catfish_dried": [
        "Catfish :dried"
    ],
    "catfish_smoked": [
        "Catfish Smoked"
    ],
    "chicken_feet": [
        "Chicken Feet",
        "Chicken feet"
    ],
    "chicken_wings": [
        "Chicken Wings"
    ],
    "chicken_frozen": [
        "Chicken meat (Frozen)",
        "Frozen chicken"
    ],
    "crayfish_small_white": [
        "Cray fish small white"
    ],
    "dried_fish": [
        "Dried Fish Sardine",
        "Dried fish, Bonga"
    ],
    "milk_evap_peak": [
        "Evaporated tinned milk(peak), 170g",
        "Tin Milk-Evaporated, Peak Milk, 150g"
    ],
    "milk_evap_other": [
        "Evaporated tinned milk carnation 170g",
        "Tin Milk-Evaporated, Three Crown Milk, 160g"
    ],
    "gari_white": [
        "Gari white,sold loose",
        "Garri white"
    ],
    "gari_yellow": [
        "Gari yellow,sold loose",
        "Garri Yellow"
    ],
    "ginger_fresh": [
        "Ginger, fresh"
    ],
    "goat_meat_bone_in": [
        "Goat Meat Bone in"
    ],
    "groundnut_oil": [
        "Groundnut oil, 75cl",
        "Groundnut oil: 1 bottle, specify bottle"
    ],
    "groundnuts_roasted": [
        "Groundnuts, roasted,75cl bottle"
    ],
    "irish_potato": [
        "Irish Potatoe",
        "Irish potato"
    ],
    "local_rice": [
        "Local Rice (Broken)",
        "Rice local sold loose",
        "Rice Local, short-Grained"
    ],
    "mackerel_frozen": [
        "Mackerel : frozen",
        "Mackerel, Frozen"
    ],
    "maize_grain_white": [
        "Maize (Corn) Grains (White) sold loose",
        "Maize grain white sold loose"
    ],
    "maize_grain_yellow": [
        "Maize grain yellow sold loose"
    ],
    "mudfish_fresh": [
        "Mudfish (aro) fresh"
    ],
    "mudfish_dried": [
        "Mudfish : dried"
    ],
    "onion": [
        "Onion bulb",
        "Onions, fresh "
    ],
    "palm_oil": [
        "Palm oil, 75cl",
        "Palm oil: 1 bottle,specify bottle"
    ],
    "plantain_ripe": [
        "Plantain (ripe)",
        "Plantain(ripe)"
    ],
    "plantain_unripe": [
        "Plantain (unripe)",
        "Plantain(unripe)"
    ],
    "rice_imported_long": [
        "Rice Long-Grained (Imported)",
        "Rice,imported high quality sold loose"
    ],
    "rice_medium": [
        "Rice Medium Grained"
    ],
    "rice_agric": [
        "Rice agric sold loose"
    ],
    "semovita_1kg": [
        "Semovita, Prepacked (1kg)"
    ],
    "smoked_fish": [
        "Smoked fish"
    ],
    "sweet_potato": [
        "Sweet potato",
        "Sweet potatoes "
    ],
    "tilapia_fresh": [
        "Tilapia fish (epiya) fresh",
        "Tilapia fresh fish (Epiya)"
    ],
    "titus_fish": [
        "Titus, frozen",
        "Titus:frozen"
    ],
    "tomato_fresh": [
        "Tomato",
        "Tomatoes, fresh "
    ],
    "veg_oil": [
        "Vegetable Oil, 75cl",
        "Vegetable oil:1 bottle,specify bottle"
    ],
    "watermelon": [
        "Watermelon whole, medium size fresh"
    ],
    "wheat_flour": [
        "Wheat Flour, Prepacked (2kg)",
        "Wheat flour: prepacked (golden penny 2kg)"
    ],
    "yam_tuber": [
        "Yam Tuber",
        "Yam tuber"
    ]
    # "region": ["Region"],
    # "state": ["State"],
    # "date": ["Date"],
    # "item_label": ["Item Label"]

}

from clean_data import Data
file = "data/bronze/SELECTED%20FOOD%20JANUARY%202023.xlsx"
file = "data/bronze/Selected%20food%20price%20watch%20feb%202016-%20proshare.xlsx"

clean_data = Data()
# df = clean_data.clean_2016_data(file)
# print(len(df.columns))
# df=clean_data.standardize_columns(df,ColumnMap)
# # df.head.to_csv('data/clean.csv')
# # print(df.iloc[1, :])
# print(df.head())
# print(len(df.columns))
# aug = "data/bronze/SELECTED%20FOOD%20AUGUST%202023.xlsx"
# aug_df = clean_data.clean_02_2023_08_2023(aug)
# print(len(aug_df.columns))
# aug_df=clean_data.standardize_columns(aug_df,ColumnMap)
# print(aug_df)
# print(len(aug_df.columns))
import json
from pathlib import Path

import re
import os

def extract_date_from_filename(data_link):
    filename = os.path.basename(data_link)

    # Map short & full month names to month numbers
    month_map = {
        'jan': '01', 'january': '01',
        'feb': '02', 'february': '02',
        'mar': '03', 'march': '03',
        'apr': '04', 'april': '04',
        'may': '05',
        'jun': '06', 'june': '06',
        'jul': '07', 'july': '07',
        'aug': '08', 'august': '08',
        'sep': '09', 'sept': '09', 'september': '09',
        'oct': '10', 'october': '10',
        'nov': '11', 'november': '11',
        'dec': '12', 'december': '12',
        'decemeber': '12'  # handle typo
    }

    # Normalize filename
    normalized = filename.lower().replace('%20', ' ').replace('_', ' ').replace('-', ' ')

    # Try: Full month + year (e.g. "march 2023")
    match1 = re.search(r'\b(' + '|'.join(month_map.keys()) + r')\s+(\d{2,4})\b', normalized)
    if match1:
        month_str = match1.group(1)
        year_str = match1.group(2)
        if len(year_str) == 2:
            year_str = '20' + year_str  # assume 21st century
        month_num = month_map.get(month_str[:3])
        return f"01/{month_num}/{year_str}"

    # Try: Compact format e.g. "jan25", "apr25"
    match2 = re.search(r'\b(' + '|'.join(month_map.keys()) + r')(\d{2})\b', normalized)
    if match2:
        month_str = match2.group(1)
        year_str = match2.group(2)
        year_str = '20' + year_str  # assume 21st century
        month_num = month_map.get(month_str[:3])
        return f"01/{month_num}/{year_str}"

    return None  # Could not extract

# === CONFIG ===
BRONZE_DIR = Path("data/bronze")
# METADATA_PATH = Path("data/bronze_metadata.json")

# # === GET ALL FILES IN BRONZE DIR ===
# metadata = {}
import pandas as pd
counter = 0
files = []
for file in BRONZE_DIR.glob("*.xlsx"):
    date_= clean_data.extract_date_from_filename(file)
    date_ = pd.to_datetime(date_, dayfirst=True)
    start = pd.Timestamp("2017-01-01")
    end = pd.Timestamp("2022-12-31")
    
# Check if date is in range
    if start <= date_ <= end:
        continue
  
    elif date_.year == 2016:
        print(f"2016\n{file}")
    elif date_.month == 1 and date_.year == 2023:
        print("2017-2023")
        print(file)
    elif date_.year == 2023 and date_.month in [4, 5, 7, 8]:
        print("April-August 2023 (excluding June)")
        print(file)

    elif date_.year == 2023 and date_.month == 6:
        print("June 2023 — Special Logic")
        print(file)

    else:
        pass