from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, desc
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

def generate_specialty_insights(spark, processed_data_path):
    df = spark.read.format("delta").load(processed_data_path)
    specialty_counts = df.groupBy("Specialty").agg(count("Name").alias("Count")).orderBy(desc("Count"))
    return specialty_counts

def build_recommendation_system(spark, processed_data_path):
    df = spark.read.format("delta").load(processed_data_path)
    als = ALS(userCol="UserId", itemCol="TherapistId", ratingCol="Rating", coldStartStrategy="drop")
    model = als.fit(df)
    return model

def identify_trends_in_ratings(spark, processed_data_path):
    df = spark.read.format("delta").load(processed_data_path)
    trends = df.groupBy("Date").agg(count("Rating").alias("Count"), avg("Rating").alias("AverageRating")).orderBy("Date")
    return trends

# Example usage:
# spark = SparkSession.builder.appName("DataPipelineInsights").getOrCreate()
# specialty_insights = generate_specialty_insights(spark, "path/to/processed/data")
# recommendation_model = build_recommendation_system(spark, "path/to/processed/data")
# rating_trends = identify_trends_in_ratings(spark, "path/to/processed/data")