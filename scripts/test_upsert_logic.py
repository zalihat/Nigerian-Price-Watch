import pandas as pd
from pathlib import Path
# file = "data\silver\selected_food_Nov_2024.parquet"
# file = "data\silver\selected_food_oct_2024.parquet"
# df = pd.read_parquet(file)
# print(df.columns)
# print(df.head())
from clean_data import Data
c = Data()
SILVER_DIR = Path("data/silver")
df_list = []
for file in SILVER_DIR.glob("*.parquet"):
    df = pd.read_parquet(file)
    df_list.append(df)
# print(df_list)
dfas = pd.concat(df_list)
# dfas = c.standardize_columns(dfs)
print(dfas.head())
print(dfas.shape)
# dfas.to_csv('all.csv')
print(dfas.isnull().sum()>0)