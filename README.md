# **Nigerian-Price-Watch**
## Problem statement
In Nigeria prices of food items increase/ decrease seasonally as harvests tend to increase supply. Nevertheless there are products that are relatively cheap or expensive in certain state/region mostly because the products are produced in the state/region
Aside from the aforementioned factors there are other factors such as cost of transportation, government and legal regulations that affect prices. 

## AIM
The aim of the project is to create a data source and a dashboard to track the price of certain products in Nigeria. 
* Traders can buy products that are cheap in certain regions and sell them in regions where they are expensive. They can also stock products(e.g Beans) when it is in season and sell later when the demand is high.
* Using the dashboard consumers can also know when certain products will be cheap and expensive and can stock up.
* Manufacturers can also use the dashboard to know where and when certain products used as raw materials are expensive and when they are not.


<!-- A data source for selected items prices in Nigeria.  -->
<!-- Data source:  -->
<!-- [National bureau of statistics ](https://nigerianstat.gov.ng/)  -->

#### ITEMS
1. Selected Food items
    * Agric eggs medium size
    * Agric eggs(medium size price of one)
    * Beans brown,sold loose
    * Beans:white black eye. sold loose
    * Beef Bone in
    * Beef,boneless
    * Bread sliced 500g
    * Bread unsliced 500g
    * Broken Rice (Ofada)
    * Chicken Feet
    * Chicken Wings
    * Evaporated tinned milk carnation 170g
    * Evaporated tinned milk(peak), 170g
    * Frozen chicken
    * Gari white,sold loose
    * Gari yellow,sold loose
    * Mudfish (aro) fresh
    * Mudfish : dried
    * Onion bulb
    * Rice agric sold loose
    * Rice local sold loose
    * Rice Medium Grained
    * Rice,imported high quality sold loose
    * Tomato
    * Yam tuber
    * Dried Fish Sardine
    * Iced Sardine
    * Irish potato
    * Sweet potato
    * Tilapia fish (epiya) fresh
    * Titus:frozen
    * Catfish (obokun) fresh
    * Catfish :dried
    * Catfish Smoked
    * Mackerel : frozen
    * Groundnut oil: 1 bottle, specify bottle
    * Maize grain white sold loose
    * Maize grain yellow sold loose
    * Palm oil: 1 bottle,specify bottle
    * Plantain(ripe)
    * Plantain(unripe)
    * Vegetable oil:1 bottle,specify bottle
    * Wheat flour: prepacked (golden penny 2kg)
2. Household Kerosene
3. Automotive gas oil(Diesel)
4. Premium Motor Spirit (Petrol)
5. Liquefied Petroleum Gas (Cooking gas)

## Data scraping
The data is scraped from the [National bureau of statistics ](https://nigerianstat.gov.ng/). The script is written using Python programming language - DataScraping/crawler.py

## Data wrangling
The data was efficiently cleaned and transformed using Python. Some of the steps are listed below:

Conversion of the data types of some variables
Fixing structural errors.
Handling missing values.
Derivation of certain features needed.
Removing duplicates.

## Dashboard
<!-- <img src="./2/to/img.jpg" alt="Dashboard /> -->

<img src="Dashboard\dasboard.PNG" alt="Dashboard" />


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






