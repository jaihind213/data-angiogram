import os

import duckdb

stats_data_path = os.environ.get('STATS_DATA_PATH', '/tmp/stats_data/')


def test_verify_state_column_in_stats_is_not_null():
    """
    - Data Completeness test -
    Verify that the state column is not null
    """
    con = duckdb.connect(database=':memory:')
    con.execute(f"""
        CREATE TABLE stats AS 
        SELECT * FROM read_parquet('{stats_data_path}/*.parquet')
    """)
    records = con.execute("SELECT count(*) FROM stats WHERE state IS NULL").fetchall()
    count = records[0][0]
    assert 0 == count, "Data Completeness test - State column should have no null values"


def test_verify_if_old_data_not_considered():
    """
    - Data Consistency test -
    Verify that the very old data like of 1970 is not considered
    """
    con = duckdb.connect(database=':memory:')
    con.execute(f"""
        CREATE TABLE stats AS 
        SELECT * FROM read_parquet('{stats_data_path}/*.parquet')
    """)
    records = con.execute("SELECT count(*) FROM stats WHERE CAST(strftime('%Y', CAST(trip_date AS DATE)) AS INTEGER) <= 2023").fetchall()
    count = records[0][0]
    assert 0 == count, "Data Consistency test - No data should be present before 2023"


def test_verify_revenue_accuracy_for_Jeep():
    """
    - Data Accuracy test -
    Verify that the revenue is accurate. it should include taxes too.
    """
    con = duckdb.connect(database=':memory:')
    con.execute(f"""
        CREATE TABLE stats AS 
        SELECT * FROM read_parquet('{stats_data_path}/*.parquet')
    """)
    records = con.execute("SELECT sum(revenue) FROM stats where car_model = 'Jeep'").fetchall()
    total_revenue = records[0][0]
    assert 20.4 == total_revenue, "Data Accuracy test - Total revenue should be 20.4 = 20.2(fare for 2 valid trips) + 0.2(tax for 2 valid trips)"
