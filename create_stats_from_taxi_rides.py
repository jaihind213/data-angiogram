import os

import duckdb

def caculate_revenue():
    # Connect to DuckDB
    con = duckdb.connect(database=':memory:')

    # Specify the path to the Parquet files
    parquet_file_path = os.environ.get('RAW_DATA_PATH', '/tmp/raw_data')
    stats_path = os.environ.get('STATS_DATA_PATH', '/tmp/stats_data/')
    os.makedirs(stats_path, exist_ok=True)

    con.execute("""
    CREATE TABLE zipcode_mapping (
        zipcode STRING,
        state STRING
    )
    """)

    # Insert records into zipcode_mapping table. WE LEAVE OUT 10004 ON PURPOSE
    con.execute("""
    INSERT INTO zipcode_mapping VALUES 
    ('10001', 'NEVADA'),
    ('10002', 'TEXAS'),
    ('10003', 'ARIZONA')
    """)

    # Read the Parquet files into a table
    con.execute(f"""
        CREATE TABLE trips AS 
        SELECT * FROM read_parquet('{parquet_file_path}/*.parquet')
    """)

    # Run the query
    # todo: fix this query to get the correct revenue by adding the tax_amount also
    query = """
        SELECT 
            trips.car_model, 
            zipcode_mapping.state, 
            trips.currency, 
            strftime('%Y-%m-%d', start_time) as trip_date,
            SUM(fare_amount) AS revenue
        FROM 
            trips
        LEFT JOIN 
            zipcode_mapping ON trips.pickup_zipcode = zipcode_mapping.zipcode
        GROUP BY 
            trips.car_model, 
            zipcode_mapping.state, 
            trips.currency, 
            strftime('%Y-%m-%d', start_time)    
            """
    result = con.execute(query).fetchdf()
    print(result)
    con.execute(f"COPY ({query}) TO '{stats_path}/stats.parquet' (FORMAT PARQUET);")

if __name__ == "__main__":
    caculate_revenue()
