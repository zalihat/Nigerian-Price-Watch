import sys

# tell interpreter where to look
sys.path.insert(0, "..")
from DataScraping.crawler import Crawler
from DataPreprocessing.Preprocess import Data
import plotly.express as px
import plotly.graph_objects as go


import pandas as pd


class Dashboard:
    # def __init__(self):
    #     self.product = product

    def get_df(self, product):
        # url = 'https://nigerianstat.gov.ng/elibrary'
        # commodity = 'food'
        # month_year = 'december 2022'
        # food_crawler = Crawler(url, commodity, month_year)
        # data_link = food_crawler.get_data_link(food_crawler.get_page_link())
        # preprocess_food = Data(data_link, 'SELECTED FOOD AUGUST 2022.xlsx')
        # df = preprocess_food.create_final_df()
        if product == "Diesel":
            df = pd.read_csv("data/diesel.csv")
            
        elif product == "Cooking gas":
            df = pd.read_csv("data/gas_data.csv")
        elif product == "Household kerosine":
            df = pd.read_csv("data/kero_data.csv")
        else:
            df = pd.read_csv("data/data.csv")
            df = df[df.Year != 1900]
        return df

    def get_states(self):
        states = [
            "ABIA",
            "ABUJA",
            "ADAMAWA",
            "AKWA IBOM",
            "ANAMBRA",
            "BAUCHI",
            "BAYELSA",
            "BENUE",
            "BORNO",
            "CROSS RIVER",
            "DELTA",
            "EBONYI",
            "EDO",
            "EKITI",
            "ENUGU",
            "GOMBE",
            "IMO",
            "JIGAWA",
            "KADUNA",
            "KANO",
            "KATSINA",
            "KEBBI",
            "KOGI",
            "KWARA",
            "LAGOS",
            "NASSARAWA",
            "NIGER",
            "OGUN",
            "ONDO",
            "OSUN",
            "OYO",
            "PLATEAU",
            "RIVERS",
            "SOKOTO",
            "TARABA",
            "YOBE",
            "ZAMFARA",
        ]
        return states

    def get_products(self):
        df = self.get_df("food")
        food_products = df.columns[1:-4]
        all_products = ['Cooking gas', 'Diesel', 'Household kerosine']
        all_products.extend(food_products)
        return all_products



def get_current_price(state, product):
    data = Dashboard()
    df = data.get_df(product) 
    df["Date"] = pd.to_datetime(df["Date"], format="%Y/%m")
    if product in ['Cooking gas', 'Diesel', 'Household kerosine']:
        price = df.loc[df.index[-1], state.title()]
    else:
        state = '_'.join(state.split(' '))
        # state = ['_'.join(state.split(' ')) for state in state]
        price = df[df.State == state][product]
        price = price.loc[price.index[-1]]
        

    return round(price,1)
def get_lowest_price(product):
    data = Dashboard()
    df = data.get_df(product) 
    if product in ['Cooking gas', 'Diesel', 'Household kerosine']:
        prices = df.loc[df.index[-1]]
        prices = prices.iloc[1:].astype('float')
        min_price = prices.min()
        min_state = prices.idxmin()
    else:
        max_month = df.Month.max()
        max_year = df.Year.max()
        df = df.query("Month == @max_month and Year == @max_year")
        df = df.groupby(['State', 'Date'])[product].max().reset_index().sort_values(by = product)
        df = df.iloc[0, :]
        min_state = df.State
        min_price = df[product]
    return '{} ({})'.format(min_state, round(min_price,1))
def get_highest_price(product):
    data = Dashboard()
    df = data.get_df(product) 
    if product in ['Cooking gas', 'Diesel', 'Household kerosine']:
        prices = df.loc[df.index[-1]]
        prices = prices.iloc[1:].astype('float')
        max_price = prices.max()
        max_state = prices.idxmax()
    else:
        max_month = df.Month.max()
        max_year = df.Year.max()
        df = df.query("Month == @max_month and Year == @max_year")
        df = df.groupby(['State', 'Date'])[product].max().reset_index().sort_values(by = product)
        df = df.iloc[-1, :]
        max_state = df.State
        max_price = df[product]

    return '{} ({})'.format(max_state, round(max_price, 1))
    



dashb = Dashboard()
df = dashb.get_df('Agric eggs medium size')
states = dashb.get_states()
products = dashb.get_products()
# print(df.Date.tail())
# print(get_current_price('ABUJA', 'Cooking gas' ))


# print(states)
# print(products)
# print(df.info())


def foodpriceGraph(state, product):
    data = Dashboard()
    df = data.get_df(product) 
    df["Date"] = pd.to_datetime(df["Date"], format="%Y/%m")
    # df.info()
    if product not in ['Cooking gas', 'Diesel', 'Household kerosine']:
        state = '_'.join(state.split(' '))
        # state = ['_'.join(state.split(' ')) for state in state]
        df = df[df['State'] ==  state]
        # df = df[df['State'].isin(state)]
        fig = px.line(df, x=df.Date, y=product, color="State")
    else:
        fig = px.line(df, x=df.Date, y =state.title(), labels={state.title(): product})
    fig.update_xaxes(
        # rangeslider_visible=True,
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        )
    )
    return fig 
def get_lowest_five(product):
    data = Dashboard()
    df = data.get_df(product) 
    df["Date"] = pd.to_datetime(df["Date"], format="%Y/%m")
    
    if product in ['Cooking gas', 'Diesel', 'Household kerosine']:
        df= df.loc[df.index[-1]]
        df = df.iloc[1:].sort_values()[:6]
        df = df.reset_index(name = 'Price')
        fig = px.bar(df, x =df['index'], y = df['Price'], title='Lowest Five states', text= df['Price'])
        # fig.update_traces(textposition="outside")
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    else:
        max_month = df.Month.max()
        max_year = df.Year.max()
        df = df.query("Month == @max_month and Year == @max_year")
        df = df.groupby(['State', 'Date'])[product].max().reset_index().sort_values(by = product)
        df = df.iloc[:6, :]
        fig = px.bar(df, x =df['State'], y = df[product], title='Lowest Five states', text = df[product])
        # fig.update_traces(textposition="outside")
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    return fig

def get_highest_five(product):
    data = Dashboard()
    df = data.get_df(product) 
    df["Date"] = pd.to_datetime(df["Date"], format="%Y/%m")
    
    if product in ['Cooking gas', 'Diesel', 'Household kerosine']:
        df= df.loc[df.index[-1]]
        df = df.iloc[1:].sort_values()[-6:]
        df = df.reset_index(name = 'Price')
        fig = px.bar(df, x =df['index'], y = df['Price'], title='Highest Five states', text= df['Price'])
        
    else:
        max_month = df.Month.max()
        max_year = df.Year.max()
        df = df.query("Month == @max_month and Year == @max_year")
        df = df.groupby(['State', 'Date'])[product].max().reset_index().sort_values(by = product)
        df = df.iloc[-6:, :]
        # df.drop('Date', axis = 1, inplace = True)
        df = df.round(1)
        # df[product] = round
        fig = px.bar(df, x =df['State'], y = df[product], title='Highest Five states', text = df[product])
        # fig = go.Figure(data=[go.Table(
        #     header=dict(values=list(df.columns),
        #                 fill_color='paleturquoise',
        #                 align='left'),
        #     cells=dict(values=[df.State, df[product]],
        #             fill_color='lavender',
        #             align='left'))
        # ])
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    return fig



