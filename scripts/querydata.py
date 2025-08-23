import duckdb

# Connect to your database
con = duckdb.connect("your_duckdb_file.duckdb")

# Simple example: Get all rows for August 2024
df = con.execute("""
    SELECT *
    FROM food_price_history
    order by date desc
""").fetchdf()

print(df.head())

# # Example: Average tomato price by region
# df_avg = con.execute("""
#     SELECT region, AVG("tomato") AS avg_tomato_price
#     FROM food_price_history
#     GROUP BY region
#     ORDER BY avg_tomato_price DESC
# """).fetchdf()

# print(df_avg)
