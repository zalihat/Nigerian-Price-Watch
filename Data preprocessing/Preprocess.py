import sys
import pandas as pd
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# tell interpreter where to look
sys.path.insert(0, "..")
from DataScraping.crawler import Crawler

url = "https://nigerianstat.gov.ng/elibrary"
commodity = "food price"
month_year = "august 2022"
food_crawler = Crawler(url, commodity, month_year)
data_link = food_crawler.get_data_link(food_crawler.get_page_link())


import pandas as pd
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class Data:
    def __init__(self, data_link):
        self.data_link = data_link

    def create_df(self, data_backup_path):
        try:
            data = pd.ExcelFile(self.data_link)
            return data
        except:
            print("Cannot reach website")
            data = pd.ExcelFile(data_backup_path)
            return data

    def get_all_states(self, kind="data", state="ABUJA"):
        path = "SELECTED FOOD AUGUST 2022.xlsx"
        data_frame = self.create_df(path)
        state = state.upper()
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
                    all_states_df = all_states_df.append(df, ignore_index=True)
                else:
                    all_states_df = pd.concat([all_states_df, df], axis=0)

            elif kind == "states":
                states = data_frame.sheet_names
                return states
            else:
                return None
        return all_states_df

    def find_Unnamed_values(self, df, column):
        counter = 0
        indices = []
        values = list(df[column].values)
        for value in values:
            if str(value).startswith("Unnamed"):
                counter = counter + 1
                index_ = values.index(value)
                indices.append(index_)
            else:
                pass
        return counter, indices

    def fix_unnamed_values(self):
        df = self.get_all_states()
        columns = df.columns
        df = df.reset_index()

        for column in columns:
            counter, indices = self.find_Unnamed_values(df, column)
            if column == "Date":
                for i in range(len(indices)):
                    index_ = df.index[indices[i]]
                    new_value = df.at[df.index[indices[i]] - 1, column] + relativedelta(
                        months=1
                    )
                    prev_value = df.at[index_, column]
                    df.loc[df[column] == prev_value, column] = str(new_value)
            else:
                for i in range(len(indices)):
                    index_ = df.index[indices[i]]
                    prev_value = df.at[index_, column]
                    df.loc[df[column] == prev_value, column] = " "
        return df.iloc[:, 1:]

    def find_typo(self, df, column):
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
        df = self.fix_unnamed_values()
        # print(df.head())
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
        df[cols_] = df[cols_].astype('float')
        return df
