from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, regexp_replace
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

def create_spark_session():
    spark = SparkSession.builder \
        .appName("ETL Transformation") \
        .getOrCreate()
    return spark

def parse_nested_json(spark, json_file_path):
    df = spark.read.json(json_file_path)
    return df

def aggregate_reviews(df):
    aggregated_df = df.groupBy("name", "location").agg(
        {"rating": "avg", "reviews": "count"}
    ).withColumnRenamed("avg(rating)", "average_rating") \
     .withColumnRenamed("count(reviews)", "review_count")
    return aggregated_df

def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    keywords = [word for word in words if word.isalnum() and word.lower() not in stop_words]
    return keywords

def standardize_location(df):
    standardized_df = df.withColumn("latitude", col("location").getField("lat")) \
                         .withColumn("longitude", col("location").getField("lon"))
    return standardized_df

def clean_data(df):
    cleaned_df = df.withColumn("name", regexp_replace(col("name"), "[^a-zA-Z0-9 ]", "")) \
                   .na.drop()
    return cleaned_df

def transform_data(json_file_path):
    spark = create_spark_session()
    df = parse_nested_json(spark, json_file_path)
    cleaned_df = clean_data(df)
    aggregated_df = aggregate_reviews(cleaned_df)
    standardized_df = standardize_location(aggregated_df)
    
    return standardized_df

if __name__ == "__main__":
    json_file_path = "data/raw/psychologists_data.json"
    transformed_data = transform_data(json_file_path)
    transformed_data.write.format("delta").mode("overwrite").save("data/processed/transformed_data")