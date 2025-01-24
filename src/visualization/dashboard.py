from pyspark.sql import SparkSession
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_heatmap(data):
    plt.figure(figsize=(12, 8))
    heatmap_data = data.pivot_table(index='Location', columns='Rating', values='Count', fill_value=0)
    sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu')
    plt.title('Heatmap of Therapists by Rating and Location')
    plt.xlabel('Rating')
    plt.ylabel('Location')
    plt.show()

def visualize_top_rated_therapists(data):
    top_therapists = data.nlargest(10, 'Rating')
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Rating', y='Name', data=top_therapists, palette='viridis')
    plt.title('Top Rated Therapists')
    plt.xlabel('Rating')
    plt.ylabel('Therapist Name')
    plt.show()

def visualize_specialty_distribution(data):
    plt.figure(figsize=(12, 6))
    specialty_counts = data['Specialty'].value_counts()
    sns.barplot(x=specialty_counts.index, y=specialty_counts.values, palette='magma')
    plt.title('Distribution of Specialties')
    plt.xlabel('Specialty')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.show()

def main():
    spark = SparkSession.builder.appName("TherapistVisualization").getOrCreate()
    processed_data_path = "data/processed/therapists_data.parquet"
    data = spark.read.parquet(processed_data_path).toPandas()

    create_heatmap(data)
    visualize_top_rated_therapists(data)
    visualize_specialty_distribution(data)

if __name__ == "__main__":
    main()