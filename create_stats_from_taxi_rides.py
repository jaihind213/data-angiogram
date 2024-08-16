import os

import duckdb

def caculate_revenue():
    # Connect to DuckDB
    con = duckdb.connect(database=':memory:')

    # Specify the path to the Parquet files
    parquet_file_path = os.environ.get('RAW_DATA_PATH', '/tmp/raw_data')
    stats_path = os.environ.get('STATS_DATA_PATH', '/tmp/stats_data/')
    os.makedirs(stats_path, exist_ok=True)

    # Read the Parquet files into a table
    con.execute(f"""
        CREATE TABLE trips AS 
        SELECT * FROM read_parquet('{parquet_file_path}/*.parquet')
    """)

    # Run the query
    query = """
        SELECT 
            car_model, currency,
            strftime('%Y-%m-%d', start_time) as dt_time, 
            SUM(fare_amount) as revenue
        FROM 
            trips 
        GROUP BY 
            car_model,currency,
            strftime('%Y-%m-%d', start_time)
    """
    result = con.execute(query).fetchdf()
    print(result)
    con.execute(f"COPY ({query}) TO '{stats_path}/stats.parquet' (FORMAT PARQUET);")

if __name__ == "__main__":
    caculate_revenue()
