# **Nigerian-Price-Watch**
A data source for selected items prices in Nigeria. 
Data source: 
[National bureau of statistics ](https://nigerianstat.gov.ng/) 

## **ITEMS**
1. Selected Food Prices Watch
2. National Household Kerosene Price watch
3. Automotive gas oil(Diesel)
4. Premium Motor Spirit (Petrol)
5. Liquefied Petroleum Gas (Cooking gas)

### **How to run**

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






