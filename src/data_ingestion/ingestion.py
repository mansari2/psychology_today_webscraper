from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import json
import os

def create_spark_session():
    spark = SparkSession.builder \
        .appName("Data Ingestion Pipeline") \
        .getOrCreate()
    return spark

def load_raw_data(spark, file_path):
    if file_path.endswith('.json'):
        return spark.read.json(file_path)
    elif file_path.endswith('.csv'):
        return spark.read.csv(file_path, header=True, inferSchema=True)
    else:
        raise ValueError("Unsupported file format")

def clean_data(df):
    # Remove rows with null values
    df = df.na.drop()
    # Additional cleaning logic can be added here
    return df

def standardize_schema(df):
    # Example schema standardization
    return df.select(
        col("name").alias("Name"),
        col("location").alias("Location"),
        col("profile_url").alias("Profile URL"),
        col("statement").alias("Statement"),
        col("phone").alias("Phone")
    )

def save_to_data_lake(df, output_path):
    df.write.mode("overwrite").parquet(output_path)

def main(raw_data_path, output_data_path):
    spark = create_spark_session()
    
    raw_data_df = load_raw_data(spark, raw_data_path)
    cleaned_df = clean_data(raw_data_df)
    standardized_df = standardize_schema(cleaned_df)
    
    save_to_data_lake(standardized_df, output_data_path)
    
    spark.stop()

if __name__ == "__main__":
    raw_data_path = os.path.join("data", "raw", "therapists_basic_data.json")  # Example path
    output_data_path = os.path.join("data", "processed", "therapists_data.parquet")  # Example path
    main(raw_data_path, output_data_path)