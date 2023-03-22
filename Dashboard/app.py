import dash
from dash import dcc, dash_table
import dash_html_components as html
import plotly.express as px
import pandas as pd
from datetime import date

# from data import getData, states, QueryNational, getCurrentPrice, foods, foodpriceGraph
from dash.dependencies import Output, Input, State
from data import (
    df,
    states,
    products,
    foodpriceGraph,
    get_highest_price,
    get_lowest_price,
    get_current_price,
    get_lowest_five,
    get_highest_five,
    MoM,
    YoY,
    month_average
)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]


# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H1(
                            children="Nigeria Price Watch",
                            # id="f",
                            style={
                                "color": "white",
                                "margin-top": "25px",
                                "font-family": "Roboto",
                            },
                        ),
                        html.P(
                            children="Last updated December 2022",
                            # id="f",
                            style={
                                "color": "white",
                                # "font-family": "Roboto"
                                "fontSize": "20px",
                            },
                        ),
                    ],
                    className="col-12",
                )
            ],
            className="row bg-success text-white mb-3",
        ),
        html.Div(
            [
                html.Div([
                    html.P(
                        children="Pick date range",
                        style={
                        # "text-align": "center",
                        # "white-space": "nowrap",
                                # "text-overflow": "ellipsis",
                                "fontSize": "20px",
                        },
                    ), 
                    dcc.DatePickerRange(
                    id='my-date-picker-range',
                    min_date_allowed=date(2015, 1, 1),
                    max_date_allowed=date(2022, 12, 1),
                    initial_visible_month=date(2022, 1, 1),
                    end_date=date(2022, 12, 1),
                    start_date=date(2022, 1, 1),
                    style={
                        "fontSize": "20px",
                    }
    ),
                ], className="col-12 col-md-6 col-lg-4 mb-3 "),
                html.Div(
                    [
                        html.P(
                        children="State",
                        style={
                        # "text-align": "center",
                        "fontSize": "20px",
                        },

                    ), 
                        dcc.Dropdown(
                            id="states-dropdown",
                            options=[{"label": i, "value": i} for i in states],
                            value=states[0],
                            placeholder="Select State",
                            # multi=True,
                            clearable=False,
                            
                            style={
                                "font-size": "20px",
                                "color": "grey",
                                "white-space": "nowrap",
                                "text-overflow": "ellipsis",
                            },
                        )
                    ],
                    className="col-12 col-md-6 col-lg-4 mb-3",
                ),
                html.Div(
                    [
                        html.P(
                        children="Product",
                        style={
                        # "text-align": "center",
                        "fontSize": "20px",
                        },

                    ), 
                        dcc.Dropdown(
                            id="product-type",
                            options=[{"label": i, "value": i} for i in products],
                            value=products[0],
                            placeholder="Select product",
                            clearable=False,
                            style={
                                "font-size": "20px",
                                "color": "grey",
                                "white-space": "nowrap",
                                "text-overflow": "ellipsis",
                            },
                        )
                    ],
                    className="col-12 col-md-6 col-lg-4 mb-3",
                ),
            ],
            className="row",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.P(
                                    children="Price",
                                    style={
                                        "color": "black",
                                        "text-align": "center",
                                        "fontSize": "20px",
                                    },
                                ),
                                html.Div([
                                    
                                        html.P(
                                    children="",
                                    id="current-price",
                                    style={"fontSize": "2em", "fontWeight": "bold"},

                                ),
                                   
                                
                                ], className="row"),
                            ],
                            className="bg-light text-dark border rounded",
                            style={
                                "height": "120px",
                                "display": "flex",
                                "flexDirection": "column",
                                "alignItems": "center",
                                "justifyContent": "center",
                            },
                        ),
                    ],
                    className="col-lg-2 mb-3",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.P(
                                    children="Lowest",
                                    # id="food-selected",
                                    style={
                                        "color": "black",
                                        "text-align": "center",
                                        "fontSize": "20px",
                                    },
                                ),
                                html.Div([
                                html.P(
                                    children="",
                                    id="lowest_price",
                                    style={"fontSize": "2em", "fontWeight": "bold"},
                                ),
                                ],
                                className="row"),
                                
                            ],
                            className="bg-light text-dark border rounded",
                            style={
                                "height": "120px",
                                "display": "flex",
                                "flexDirection": "column",
                                "alignItems": "center",
                                "justifyContent": "center",
                                # "text-align": "justify",
                                # "background-color" :"rgb(255,240,245)",
                            },
                        ),
                    ],
                    className="col-lg-3 mb-3",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.P(
                                    children="Highest",
                                    # id="food-selected",
                                    style={
                                        "color": "black",
                                        "text-align": "center",
                                        "fontSize": "20px",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.P(
                                            children="",
                                            id="highest-price",
                                            style={
                                                "fontSize": "2em",
                                                "fontWeight": "bold",
                                            },
                                        ),
                                        
                                    ],
                                    className="row",
                                ),
                            ],
                            className="bg-light text-dark text-dark border rounded",
                            style={
                                "height": "120px",
                                "display": "flex",
                                "flexDirection": "column",
                                "alignItems": "center",
                                "justifyContent": "center",
                            },
                        ),
                    ],
                    className="col-lg-3 mb-3",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.P(
                                    children="MoM",
                                    # id="food-selected",
                                    style={
                                        "color": "black",
                                        "text-align": "center",
                                        "fontSize": "20px",
                                    },
                                ),
                                html.P(
                                    children="",
                                    id="MoM",
                                    style={"fontSize": "2em", "fontWeight": "bold"},
                                ),
                            ],
                            className="bg-light text-dark text-dark border rounded",
                            style={
                                "height": "120px",
                                "display": "flex",
                                "flexDirection": "column",
                                "alignItems": "center",
                                "justifyContent": "center",
                            },
                        ),
                    ],
                    className="col-lg-2 mb-3",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.P(
                                    children="YoY",
                                    # id="food-selected",
                                    style={
                                        "color": "black",
                                        "text-align": "center",
                                        "fontSize": "20px",
                                    },
                                ),
                                html.P(
                                    children="",
                                    id="YoY",
                                    style={"fontSize": "2em", "fontWeight": "bold"},
                                ),
                            ],
                            className="bg-light text-dark text-dark border rounded",
                            style={
                                "height": "120px",
                                "display": "flex",
                                "flexDirection": "column",
                                "alignItems": "center",
                                "justifyContent": "center",
                            },
                        ),
                    ],
                    className="col-lg-2 mb-3",
                ),
            ],
            className="row",
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id="foodPrice-graph",
                        )
                    ],
                    className="col-12 mb-3",
                ),
            ],
            className="row",
        ),
        html.Div(
            [
                html.Div(
                    [
                        # html.P(
                        #     children= "Lowest Five states"
                        # ),
                        dcc.Graph(
                            id="monthly-average",
                        )
                    ],
                    className="col-lg-4 col-12 col-md-12 mb-3",
                ),
             html.Div(
                    [
                        # html.P(
                        #     children= "Lowest Five states"
                        # ),
                        dcc.Graph(
                            id="lowest-5",
                        )
                    ],
                    className="col-lg-4 col-12 col-md-12 mb-3",
                ),
            html.Div(
                    [
                        # html.P(
                        #     children= "Lowest Five states"
                        # ),
                        dcc.Graph(
                            id="highest-5",
                        )
                    ],
                    className="col-lg-4 col-12 col-md-12 mb-3",
                ),
            ],
            className="row",
        ),
    ],
    className="container-fluid mt-5",
    style={"background-color": "rgb(245,245,245)"},
)


@app.callback(
    Output("foodPrice-graph", "figure"),
    Input("states-dropdown", "value"),
    Input("product-type", "value"),
)
def pricegraph(state, product):
    fig = foodpriceGraph(state, product)
    return fig


@app.callback(
    Output("lowest-5", "figure"),
    # Input("states-dropdown", "value"),
    Input("product-type", "value"),
)
def lowest_five( product):
    fig = get_lowest_five( product)
    return fig

@app.callback(
    Output("highest-5", "figure"),
    # Input("states-dropdown", "value"),
    Input("product-type", "value"),
)
def highest_five( product):
    fig = get_highest_five( product)
    return fig

@app.callback(
    Output("monthly-average", "figure"),
    Input("states-dropdown", "value"),
    Input("product-type", "value"),
)
def update_monthly_avg(state, product):
    fig = month_average( state, product)
    return fig


@app.callback(
    Output("current-price", "children"),
    Input("states-dropdown", "value"),
    Input("product-type", "value"),
)
def current_price(state, product):
    current_price = get_current_price(state, product)
    return current_price


@app.callback(
    Output("lowest_price", "children"),
    # Input("states-dropdown", "value"),
    Input("product-type", "value"),
)
def lowest_price(product):
    lowest = get_lowest_price(product)
    return lowest


@app.callback(
    Output("highest-price", "children"),
    # Input("states-dropdown", "value"),
    Input("product-type", "value"),
)
def highest_price(product):
    highest = get_highest_price(product)
    return highest

@app.callback(
    Output("MoM", "children"),
    Input("states-dropdown", "value"),
    Input("product-type", "value"),
)
def Update_MoM(state, product):
    perc = MoM(state , product)
    return perc
@app.callback(
    Output("YoY", "children"),
    Input("states-dropdown", "value"),
    Input("product-type", "value"),
)
def Update_YoY(state, product):
    perc = YoY(state , product)
    return perc


if __name__ == "__main__":
    app.run_server(debug=True)
