import pandas as pd
try:
    link2 = "./data/raw/Selected%20food%20price%20watch%20feb%202016-%20proshare.xlsx"

    data = pd.ExcelFile(link2)
    df = data.parse("ABUJA")
    print(df.head())
except Exception as err:
    print(f"Unexpected {err=}, {type(err)=}")
# import os
# link = "./data/raw/SELECTED%20FOOD%20JANUARY%202023.xlsx"
# link2 = "./data/raw/Selected%20food%20price%20watch%20feb%202016-%20proshare.xlsx"
# from Preprocess import Data
# data = Data(link2, '')
# df = data.create_final_df()
# # path = os.makedirs("data/transformed")
# path = "data/transformed"
# print(df.tail())
# df.to_excel(os.path.join(path, "Jan2016to2017"))