import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType

# this program is for demonstration purposes only

kafka_topic = os.environ.get('TAXI_TOPIC', 'taxi_rides')
kafka_bootstrap_servers = os.environ.get('KAFKA_BROKER_URL', 'localhost:9092')
output_dir = os.environ.get('RAW_DATA_PATH', '/tmp/raw_data')
def run_job():
    # Initialize Spark session
    # set SPARK_HOME environment variable to point to the Spark installation directory
    # export SPARK_HOME=/Users/vishnuch/work/utils/spark-3.4.0-bin-hadoop3
    #.config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1") \

    # local testing getting ClassNotFoundException: scala.$less$colon$less
    # with kafka-0-10_2.13:3.4.0
    # trying kafka-0-10_2.12:3.4.0
    spark = SparkSession.builder \
        .appName("KafkaToParquetBatch") \
        .master(os.environ.get("SPARK_MASTER", "local[*]")) \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:3.4.0") \
        .getOrCreate()
        #.config("spark.local.dir", tmp_dir) \



    # Read data from Kafka
    df = spark \
        .read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", kafka_topic) \
        .option("startingOffsets", "earliest") \
        .option("endingOffsets", "latest") \
        .load()

    # Define the schema for the Kafka message value
    message_schema = StructType([
        StructField("taxi_id", StringType()),
        StructField("pax_id", StringType()),
        StructField("start_time", TimestampType()),
        StructField("end_time", TimestampType()),
        StructField("pickup_zipcode", StringType()),
        StructField("dropoff_zipcode", StringType()),
        StructField("tax_amount", FloatType()),
        StructField("fare_amount", FloatType()),
        StructField("currency", StringType()),
        StructField("car_model", StringType())
    ])

    # Parse the Kafka message value
    parsed_df = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), message_schema).alias("data")) \
        .select("data.*")

    # todo: dedup the data :) thats a test scenario to test also.
    # Write the data to Parquet
    parsed_df.write.mode("overwrite").parquet(output_dir)

    # Stop the Spark session
    spark.stop()
    print("Job completed successfully. read kafka & saved to parquet at path: ", output_dir)


if __name__ == "__main__":
    run_job()