import sys
from datetime import date, datetime

# import click
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
import re
import os

# tell interpreter where to look
# sys.path.insert(0, "..")
# from DataScraping.crawler import Crawler


class CleanData:
    def assign_regions_and_dates(self,df):
        # Define regions using a dictionary
        region_map = {
            "North_Central": ["Benue", "ABUJA", "Kogi", "Kwara", "NASARAWA", "Niger", "Plateau"],
            "North_East": ["Adamawa", "Bauchi", "Borno", "Gombe", "Taraba", "Yobe"],
            "North_West": ["Kaduna", "Katsina", "Kano", "Kebbi", "Sokoto", "Jigawa", "Zamfara"],
            "South_East": ["Abia", "Anambra", "Ebonyi", "Enugu", "Imo"],
            "South_South": ["Akwa Ibom", "Bayelsa", "Cross River", "Delta", "Edo", "Rivers"],
            "South_West": ["Ekiti", "Lagos", "Osun", "Ondo", "Ogun", "Oyo"],
            "NATIONAL": ["NATIONAL"]
        }

        # Convert all states in the map to uppercase
        region_map = {region: [state.upper() for state in states] for region, states in region_map.items()}

        # Uppercase state names in the DataFrame for consistent matching
        # df = df.copy()
        df["State"] = df["State"].str.upper()

        # Map state to region
        state_to_region = {
            state: region
            for region, states in region_map.items()
            for state in states
        }

        # Add region
        df["Region"] = df["State"].map(state_to_region).fillna("Unknown")

        # Convert 'Date' column to datetime if not already
        if not pd.api.types.is_datetime64_any_dtype(df["Date"]):
            df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

        return df

    def extract_date_from_filename(self,data_link):
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

    def clean_2016_data(self,data_link):
        data = pd.ExcelFile(data_link)
        states = data.sheet_names[1:]
        df_list = []
        for state in states:
            df = data.parse(state, skiprows=2)
            cols_to_drop = ['Unit of Measurement', " (Feb 2016 & Feb 2017)",  "(Jan 2017 & Feb 2017)"]
            df.drop(cols_to_drop, axis=1, inplace=True)
            df = df.transpose()
            df.columns = df.iloc[0]
            df = df.iloc[1:, :].reset_index()
            df["State"]= state.replace('_', ' ').upper()
            df.rename(columns={'index': 'Date'}, inplace=True)
            df_list.append(df)
        combined_df = pd.concat(df_list, axis=0)
        columns_to_convert = combined_df.columns[1:-1]
        # print(columns_to_convert)
        # Convert to float
        combined_df[columns_to_convert] = combined_df[columns_to_convert].astype(float)
        combined_df = self.assign_regions_and_dates(combined_df)
        combined_df = self.standardize_columns(combined_df)
        return combined_df

    def clean_01_2017_01_2023(self,data_link):
        data = pd.ExcelFile(data_link)

        all_states_df_list = []
        for state in data.sheet_names[1:]:
            df = data.parse(state)
            dfT = df.transpose()
            dfT.columns = dfT.iloc[0, :]
            dfT.head()
            df = dfT.iloc[1:,].copy()
            df.loc[:, "State"] = state
            df.index.names = ["Date"]
            df.reset_index(inplace=True)
            all_states_df_list.append(df)
        all_states_df = pd.concat(all_states_df_list, axis=0)
        all_states_df = self.fix_unnamed_values(all_states_df)
        all_states_df = self.fix_typos(all_states_df)
        all_states_df = self.assign_regions_and_dates(all_states_df)
        all_states_df = self.standardize_columns(all_states_df)
        return all_states_df
    def clean_02_2023_08_2023(self,data_link):
        data = pd.ExcelFile(data_link)
        data.sheet_names
        sheet_lookup = [s for s in data.sheet_names if s.lower() in {"states", "state", "state & zone", "states & zones"}]
        if sheet_lookup:
            df = data.parse(sheet_lookup[0], skiprows=1)
        else:
            raise ValueError("No sheet named 'STATE' or 'STATES' found (case-insensitive).")
        df = df.loc[:, ~df.columns.str.upper().str.startswith("AV")]
        df = df.transpose().reset_index()
        df.columns = df.iloc[0,:]
        df.rename(columns={'ITEMS': 'State','items': 'State' }, inplace=True)
        df= df.iloc[1:, :]
        df = self.fix_unnamed_values(df)
        df = self.fix_typos(df)
        df['Date'] = self.extract_date_from_filename(data_link)
        try:
          df = self.assign_regions_and_dates(df)
        except:
          pass
        df = self.standardize_columns(df)
        return df
    def clean_june_2023(self,data_link):
        data = pd.ExcelFile(data_link)
        data.sheet_names
        df = data.parse('SELECTED FOOD JUNE 2023', skiprows=1)
        df = df.iloc[:, -7:]
        df = df.transpose().reset_index()
        df.columns = df.iloc[0,:]
        df.rename(columns={'Items.1': 'Region'}, inplace=True)
        df= df.iloc[1:, :]
        df = self.fix_unnamed_values(df)
        df = self.fix_typos(df)
        df['Date'] = self.extract_date_from_filename(data_link)
        df = self.standardize_columns(df)
        return df
    def clean_incremental(self,data_link):
        data = pd.ExcelFile(data_link)
        data.sheet_names
        # df = data.parse("ZONE ALL ITEM")
        df = data.parse(next(s for s in data.sheet_names if s.lower() == "zone all item"))

        df = df.transpose().reset_index()
        df.columns = df.iloc[0,:]
        # df.rename(columns={'ITEM LABEL': 'Region'}, inplace=True)
        # df.rename(columns={col: "Region" for col in df.columns if col.strip().lower() == "item label"}, inplace=True)
        df.rename(
        columns={
                col: "Region"
                for col in df.columns
                if col.strip().lower() in {"row labels", "item labels", "item label"}
            },
            inplace=True
        )

        df= df.iloc[1:, :]
        df = self.fix_unnamed_values(df)
        df = self.fix_typos(df)
        df['Date'] = self.extract_date_from_filename(data_link)
        df = self.standardize_columns(df)
        return df
    def clean_column(self,col):
        col = col.lower()
        col = re.sub(r"[^\w\s]", "", col)  # Remove punctuation
        col = re.sub(r"\s+", " ", col).strip()  # Normalize whitespace
        return col

    def standardize_columns(self,df: pd.DataFrame) -> pd.DataFrame:
        # 1. Normalize all column names
        column_map =  {
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
        "Tomatoes, fresh ",
        "tomato"
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
    ],
    # "Region": ["Region", "Row Labels"],
    # "state": ["State"],
    # "date": ["Date"],
    # "item_label": ["Item Label"]

}
        original_to_cleaned = {col: self.clean_column(col) for col in df.columns}
        df = df.rename(columns=original_to_cleaned)

        # 2. Invert the cleaned name map for potential reverse lookup
        cleaned_columns = set(df.columns)

        # 3. Consolidate columns using the mapping
        for new_col, variants in column_map.items():
            variants = [self.clean_column(c) for c in variants]
            existing_variants = [self.clean_column(c) for c in variants if self.clean_column(c) in cleaned_columns]

            if not existing_variants:
                continue  # Skip if none of the variants are present

            # Use first non-null value across the variants
            df[new_col] = df[existing_variants].apply(pd.to_numeric, errors='coerce').bfill(axis=1).iloc[:, 0]

            # Drop old variants
            cols_to_drop = [col for col in existing_variants if col != new_col]
            df.drop(columns=cols_to_drop, inplace=True)

        return df

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

    def fix_unnamed_values(self, df):
        """
        Function to fix all the unnamed values in the dataset
        :return: a dataframe with no unnamed value.
        """
        # df = self.get_all_states()
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

    def fix_typos(self, df):
        """
        Function to fix all the values with typo in the dataset
        :return: a dataframe with no values with typo
        """
        # df = self.fix_unnamed_values(df)
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







