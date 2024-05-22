# **Nigerian-Price-Watch**

## Overview
This project is a price tracker for various products in Nigeria. It scrapes data from multiple sources, cleans the data using Python, and visualizes it through a dashboard created using Power BI.

## Features



**Data scraping**: Python scripts ([DataScraping](https://github.com/zalihat/Nigerian-Price-Watch/tree/master/DataScraping)) are used to scrape data from [National bureau of statistics ](https://nigerianstat.gov.ng/) 

**Data cleaning**: The scraped data is cleaned and processed to remove duplicates, handle missing values, and standardize formats

**Dashboard**: A Power BI dashboard is created to visualize the cleaned data and track the prices of different products over time

## Requirements

 * Python 3
 * Libraries: [requirements.txt](https://github.com/zalihat/Nigerian-Price-Watch/blob/master/requirements.txt)
 * Power BI Desktop (for viewing/editing the dashboard)
 
 ## Installation
 
 1. Clone the repository: git clone https://github.com/zalihat/Nigerian-Price-Watch.git
 
 2. Install dependencies: pip install -r requirements.txt
 
 3. Open the Power BI dashboard file (.pbix) using Power BI Desktop

 ## Usage
 
 1. Run the Python scripts to scrape and clean the data.
 2. Open the Power BI dashboard to visualize the cleaned data.
<!-- <img src="./2/to/img.jpg" alt="Dashboard /> -->

<!-- <img src="Dashboard\dasboard.PNG" alt="Dashboard" /> -->


## To get the dataset

```
pip install -r requirements.txt
```
```
cd DataPreprocessing
```

```
python Preprocess.py URL COMMODITY MONTH YEAR DATA_BACKUP_PATH PATH_OR_BUFFER
````

<p>Example</p>

To get the price of selected food for december 2022
```
python Preprocess.py "https://nigerianstat.gov.ng/elibrary"  "food" "december" 2022 "SELECTED FOOD DECEMEBER 2022.xlsx" "data.csv"

```



## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## Acknowledgements

Thanks to https://nigerianstat.gov.ng for providing the data.



