"""
Nigerian price watch data preprocessing  script
How to run the script:
*  python Preprocess.py 
URL
COMMODITY
MONTH
YEAR
DATA BACKUP PATH
PATH OR BUFFER

How to run using the default arguments
python Preprocess.py "https://nigerianstat.gov.ng/elibrary" 
"food" "december" 2022 "SELECTED FOOD DECEMEBER 2022.xlsx" "data.csv"
"""

import sys
from datetime import date, datetime

# import click
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

# tell interpreter where to look
# sys.path.insert(0, "..")
# from DataScraping.crawler import Crawler


class Data:
    def __init__(self, data_link, data_backup_path):
        self.data_link = data_link
        self.data_backup_path = data_backup_path

    def create_df(self):
        """
        Function creates a data frame using the data source url or the data source directory

        :param data_backup_path: backup data directory
        :return: returns a dataframe
        """

        try:
            data = pd.ExcelFile(self.data_link)
            return data
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            data = pd.ExcelFile(self.data_backup_path)
            return data

    def get_all_states(self, kind: str = "data", state: str = "ABUJA"):
        """
        Function to get all dataset for all the states and list of available state names

        :param kind: indicates what to return the dataset or the list of states.
        :return: returns a dataframe for all the states or list of states
        """
        data_frame = self.create_df()
        state = state.upper()
        # Read data for each sheet(state) and then create a dataframe containing all sheets data
        all_states_df = pd.DataFrame()
        for state in data_frame.sheet_names[1:]:
            if kind == "data":

                df = data_frame.parse(state)
                dfT = df.transpose()
                dfT.columns = dfT.iloc[0, :]
                dfT.head()
                df = dfT.iloc[
                    1:,
                ]
                df.loc[:, "State"] = state
                df.index.names = ["Date"]
                df.reset_index(inplace=True)
                if all_states_df.shape[0] == 0:
                    all_states_df = pd.concat([all_states_df, df], axis=0)
                else:
                    all_states_df = pd.concat([all_states_df, df], axis=0)
            # Get all available sheetnames(states)
            elif kind == "states":
                states = data_frame.sheet_names
                return states
            else:
                return None
        return all_states_df

    def find_Unnamed_values(self, df: str, column: str):
        """
        Function to find all the unnamed values in a column
        :param df: dataframe for all the states.
        :param column: column to check for unnamed value
        :return: The number of unnamed values (counter) and their indices
        """
        counter = 0
        indices = []
        values = list(df[column].values)
        for value in values:
            # Get all the values that starts with unnamed in the column
            if str(value).startswith("Unnamed"):
                counter = counter + 1
                index_ = values.index(value)
                indices.append(index_)
            else:
                pass
        return counter, indices

    def fix_unnamed_values(self):
        """
        Function to fix all the unnamed values in the dataset
        :return: a dataframe with no unnamed value.
        """
        df = self.get_all_states()
        columns = df.columns
        df = df.reset_index()

        for column in columns:
            counter, indices = self.find_Unnamed_values(df, column)
            if column == "Date":
                for i in range(len(indices)):
                    index_ = df.index[
                        indices[i]
                    ]  # Replace the missing date by adding a month to the previous date (data is stored monthly)
                    new_value = df.at[df.index[indices[i]] - 1, column] + relativedelta(
                        months=1
                    )
                    prev_value = df.at[index_, column]
                    df.loc[df[column] == prev_value, column] = str(new_value)
            else:
                for i in range(len(indices)):
                    index_ = df.index[indices[i]]
                    prev_value = df.at[index_, column]
                    # replace with empty
                    df.loc[df[column] == prev_value, column] = " "
        return df.iloc[:, 1:]

    def find_typo(self, df: str, column: str):
        """
        Function to find all the values with typo in a column
        :param df: dataframe for all the states.
        :param column: column to check for values with typo
        :return: The number of values with typo (counter) and their indices
        """
        counter = 0
        indices = []
        values = list(df[column].values)
        for value in values:
            l1 = str(value).split(".")
            if (
                str(value).startswith(".")
                or "," in str(value)
                or str(value).startswith("`")
                or str(value) == ","
                or str(value).endswith(".")
                or ".." in str(value)
                or " " in str(value)
                or len(l1) > 2
            ):
                counter = counter + 1
                index_ = values.index(value)
                indices.append(index_)
            else:
                pass
        return counter, indices

    def fix_typos(self):
        """
        Function to fix all the values with typo in the dataset
        :return: a dataframe with no values with typo
        """
        df = self.fix_unnamed_values()
        columns = df.columns[1:]
        for column in columns:
            counter, indices = self.find_typo(df, column)

            if counter != 0:
                for i in range(len(indices)):
                    index_ = df.index[indices[i]]
                    prev_value = df.at[index_, column]
                    if str(prev_value).startswith("`"):
                        new_value = str(prev_value).replace("`", "").rstrip(".")
                        new_value = new_value.rstrip(".")
                    elif str(prev_value).endswith("."):
                        new_value = str(prev_value).rstrip(".")
                        print(new_value)
                    elif ".." in str(prev_value):
                        new_value = ".".join(str(prev_value).split(".")[::2])
                    elif " " in str(prev_value):
                        new_value = ".".join(prev_value.split(" "))
                    elif len(str(prev_value).split(".")) > 2:
                        new_value = ".".join(str(prev_value).split(".")[:-1])
                    else:
                        new_value = (
                            str(prev_value)
                            .strip(".")
                            .replace(",", ".")
                            .replace("`", ".")
                            .replace(" ", ".")
                        )
                        new_value = ".".join(new_value.split(" "))
                    df.loc[df[column] == prev_value, column] = float(new_value)
            else:
                pass
        cols_ = list(columns[:-1])
        df[cols_] = df[cols_].astype("float")

        return df

    def create_final_df(self):
        """
        Function create the final dataframe, which will include new columns (Region, Month, year )
        :return: The final dataframe after preprocessing
        """
        # states and geo political regions
        North_Central = [
            "Benue",
            "ABUJA",
            "Kogi",
            "Kwara",
            "NASSARAWA",
            "Niger",
            "Plateau",
        ]
        North_Central = [x.upper() for x in North_Central]
        North_East = ["Adamawa", "Bauchi", "Borno", "Gombe", "Taraba", "Yobe"]
        North_East = [x.upper() for x in North_East]
        North_West = [
            "Kaduna",
            "Katsina",
            "Kano",
            "Kebbi",
            "Sokoto",
            "Jigawa",
            "Zamfara",
        ]
        North_West = [x.upper() for x in North_West]
        South_East = ["Abia", "Anambra", "Ebonyi", "Enugu", "Imo"]
        South_East = [x.upper() for x in South_East]
        South_South = ["Akwa_Ibom", "Bayelsa", "Cross_River", "Delta", "Edo", "Rivers"]
        South_South = [x.upper() for x in South_South]
        South_West = ["Ekiti", "Lagos", "Osun", "Ondo", "Ogun", "Oyo"]
        South_West = [x.upper() for x in South_West]
        df = self.fix_typos()
        # return df
        df["Date"] = pd.to_datetime(df["Date"])
        df["Month"] = df["Date"].dt.month
        df["Year"] = df["Date"].dt.year
        conditions = [
            df.State.isin(North_Central),
            df.State.isin(North_East),
            df.State.isin(North_West),
            df.State.isin(South_East),
            df.State.isin(South_South),
            df.State.isin(South_West),
            df.State == "NATIONAL",
        ]

        # create a list of the values we want to assign for each condition
        regions = [
            "North_Central",
            "North_East",
            "North_West",
            "South_East",
            "South_South",
            "South_West",
            "NATIONAL",
        ]
        df["Region"] = np.select(conditions, regions, default="Unknown")
        df.to_csv('data/clean.csv')
        return df


class CookingGas(Data):
    def get_all_states(self):
        gas_df = self.create_df()
        sheet_names = gas_df.sheet_names
        gas_5kg = gas_df.parse(sheet_names[1])
        gas_5kg = gas_5kg.iloc[2:, :]
        gas_5kg.columns = gas_5kg.iloc[0, :]
        gas_5kg = gas_5kg.iloc[1:, :]
        gas_5kg.drop("ITEM LABEL", inplace=True, axis=1)
        dfT = gas_5kg.transpose()
        dfT.head()
        dfT.columns = dfT.iloc[0, :]
        dfT.head()
        df = dfT.iloc[
            1:,
        ]
        df.index.names = ["Date"]
        df.reset_index(inplace=True)
        df = df.loc[:, :"Zamfara"]
        df["Date"] = pd.to_datetime(df["Date"], format="%Y/%m")
        df.iloc[:, 1:] = df.iloc[:, 1:].astype(float)
        gas_kg = df.copy()
        gas_kg.iloc[:, 1:] = (gas_kg.iloc[:, 1:] / 5).round(1)
        return gas_kg


class HouseholdKerosene(Data):
    def get_all_states(self):
        kero_df = self.create_df()
        sheet_names = kero_df.sheet_names
        kero_df = kero_df.parse(sheet_names[1])
        kero_df = kero_df.iloc[2:, :]
        kero_df.columns = kero_df.iloc[0, :]
        kero_df = kero_df.iloc[1:, :]
        kero_df.drop(["ITEMLABELS", "Unit of Measure"], inplace=True, axis=1)
        dfT = kero_df.transpose()
        dfT.head()
        dfT.columns = dfT.iloc[0, :]
        dfT.head()
        df = dfT.iloc[
            1:,
        ]
        df.index.names = ["Date"]
        df.reset_index(inplace=True)
        df = df.loc[:, :"Zamfara"]
        df["Date"] = pd.to_datetime(df["Date"], format="%Y/%m")
        df.iloc[:, 1:] = df.iloc[:, 1:].astype(float)
        kero_df = df.copy()
        kero_df.iloc[:, 1:] = (kero_df.iloc[:, 1:]).round(1)
        return kero_df


class Diesel(Data):
    def get_all_states(self):
        diesel_df = self.create_df()
        sheet_names = diesel_df.sheet_names
        diesel_df = diesel_df.parse(sheet_names[1])
        diesel_df = diesel_df.iloc[2:, :]
        diesel_df.columns = diesel_df.iloc[0, :]
        diesel_df = diesel_df.iloc[1:, :]
        diesel_df.drop(["ITEMLABELS"], inplace=True, axis=1)
        dfT = diesel_df.transpose()
        dfT.head()
        dfT.columns = dfT.iloc[0, :]
        dfT.head()
        df = dfT.iloc[
            1:,
        ]
        df.index.names = ["Date"]
        df.reset_index(inplace=True)
        df = df.loc[:, :"Zamfara"]
        df["Date"] = pd.to_datetime(df["Date"], format="%Y/%m")
        df.iloc[:, 1:] = df.iloc[:, 1:].astype(float)
        df.iloc[:, 1:] = (df.iloc[:, 1:]).round(1)
        return df


# @click.command()
# @click.argument("url", type=str)
# @click.argument("commodity", type=str)
# @click.argument("month", type=str)
# @click.argument("year", type=int)
# @click.argument("data_backup_path", type=str)
# @click.argument("path_or_buf", type=str)
# def main(
#     url: str,
#     commodity: str,
#     month: str,
#     year: int,
#     data_backup_path: str,
#     path_or_buf: str,
# ) -> None:
#     """
#     The main function
#     :param url: the nigerian national bureau of statistics website url
#     :param commodity: commodity of interest (food, PMS_Fuel)
#     :param month_year: month_year of interest.
#     :param path_or_buf: month_year of interest.
#     :return: None
#     """
#     month_year = " ".join([str(month).replace("'", ""), str(year).replace("'", "")])
#     commodity = str(commodity).lower().replace("'", "")
#     url = str(url).replace("'", "")
#     path_or_buf = str(path_or_buf).replace("'", "")
#     data_backup_path = str(data_backup_path).replace("'", "")
#     if commodity == "food":
#         commodity = "".join([commodity, "prices"])
#         food_crawler = Crawler(url, commodity, month_year)
#         page_link = food_crawler.get_page_link()
#         data_link = food_crawler.get_data_link(page_link)
#         preprocess_food = Data(data_link, data_backup_path)
#         df = preprocess_food.create_final_df()
#     elif commodity == "cookinggas":
#         gas_crawler = Crawler(url, commodity, month_year)
#         page_link = gas_crawler.get_page_link()
#         data_link = gas_crawler.get_data_link(page_link)
#         process_cooking_gas = CookingGas(data_link, data_backup_path)
#         df = process_cooking_gas.fix_typos()
#     elif commodity == "householdkerosene":
#         kero_crawler = Crawler(url, commodity, month_year)
#         page_link = kero_crawler.get_page_link()
#         data_link = kero_crawler.get_data_link(page_link)
#         process_cooking_kero = HouseholdKerosene(data_link, data_backup_path)
#         df = process_cooking_kero.fix_typos()
#     elif commodity == "diesel":
#         diesel_crawler = Crawler(url, commodity, month_year)
#         page_link = diesel_crawler.get_page_link()
#         data_link = diesel_crawler.get_data_link(page_link)
#         process_cooking_diesel = Diesel(data_link, data_backup_path)
#         df = process_cooking_diesel.fix_typos()
#     else:
#         pass
#     print(df.head())
#     df.to_csv(path_or_buf, index=None)


# if __name__ == "__main__":
#     main()
