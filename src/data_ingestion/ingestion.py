from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os

def create_spark_session():
    """Create a Spark session."""
    spark = SparkSession.builder \
        .appName("Data Ingestion Pipeline") \
        .getOrCreate()
    return spark

def load_raw_data(spark, file_path):
    """Load raw data from a JSON file."""
    if file_path.endswith('.json'):
        return spark.read.option("multiLine", True).json(file_path)
    elif file_path.endswith('.csv'):
        return spark.read.csv(file_path, header=True, inferSchema=True)
    else:
        raise ValueError("Unsupported file format")

def clean_data(df):
    """Clean the data by removing null rows."""
    return df.na.drop()

def standardize_schema(df):
    """Standardize the schema for consistent processing."""
    return df.select(
        col("name").alias("Name"),
        col("location").alias("Location"),
        col("profile_url").alias("Profile_URL"),
        col("statement").alias("Statement"),
        col("phone").alias("Phone")
    )

def save_to_data_lake(df, output_path):
    """Save the processed data to the data lake in Parquet format."""
    df.write.mode("overwrite").parquet(output_path)

def main(raw_data_path, output_data_path):
    """Main function to orchestrate the ingestion pipeline."""
    # Create Spark session
    spark = create_spark_session()

    # Load raw data
    raw_data_df = load_raw_data(spark, raw_data_path)

    # Clean data
    cleaned_df = clean_data(raw_data_df)

    # Standardize schema
    standardized_df = standardize_schema(cleaned_df)

    # Save to data lake
    save_to_data_lake(standardized_df, output_data_path)

    # Stop Spark session
    spark.stop()

if __name__ == "__main__":
    # Define paths
    raw_data_path = os.path.join("data", "raw", "therapists_basic_data.json")
    output_data_path = os.path.join("data", "processed", "therapists_data.parquet")

    # Run the pipeline
    main(raw_data_path, output_data_path)
