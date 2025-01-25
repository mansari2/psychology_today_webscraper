# Psychology Today Webscraper

This project aims to build a scalable data pipeline to scrape, process, and analyze data from websites listing psychologists and therapists. The pipeline integrates multiple tools and frameworks, leveraging Spark/Databricks for ETL processing and analytics.

## Project Structure

```
data-pipeline-project
├── src
│   ├── web_scraping          # Contains web scraping scripts
│   ├── data_ingestion        # Contains data ingestion scripts
│   ├── etl_transformation    # Contains ETL transformation scripts
│   ├── analytics             # Contains analytics scripts
│   ├── visualization          # Contains visualization scripts
│   └── pipeline_automation    # Contains automation scripts
├── data
│   ├── raw                   # Stores raw scraped data
│   └── processed             # Stores processed data
├── notebooks                 # Contains Jupyter notebooks for analysis and ML
├── configs                   # Contains configuration files
├── requirements.txt          # Lists project dependencies
├── README.md                 # Project documentation
└── .gitignore                # Specifies files to ignore in version control
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd data-pipeline-project
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Configure settings:**
   Update the `configs/config.yaml` file with your specific configuration settings, such as database connections and API keys.

## Usage

- **Web Scraping:**
  - Use the scripts in `src/web_scraping` to scrape data from target websites.
  
- **Data Ingestion:**
  - Run `src/data_ingestion/ingestion.py` to clean and load the raw data into the data lake.

- **ETL Transformation:**
  - Execute `src/etl_transformation/transformation.py` to transform the data for analysis.

- **Analytics:**
  - Use `src/analytics/insights.py` to generate insights from the processed data.

- **Visualization:**
  - Run `src/visualization/dashboard.py` to create visualizations of the insights.

- **Pipeline Automation:**
  - Schedule the pipeline using `src/pipeline_automation/automation.py`.

## Notebooks

- Explore data analysis and insights generation in `notebooks/data_analysis.ipynb`.
- Build and evaluate machine learning models in `notebooks/ml_model.ipynb`.

## Key Features

- **Scalability:** Utilizes Spark for distributed processing of large datasets.
- **Resilience:** Delta Lake ensures data consistency with ACID transactions.
- **Automation:** Apache Airflow or Databricks Workflows for scheduling and monitoring.
- **Visualization:** Real-time dashboards for actionable insights.

## Example Output

- **Dataset:**
  | Name                   | Location         | Rating | Reviews | Specialty                     | Contact Info      |
  |------------------------|------------------|--------|---------|-------------------------------|--------------------|
  | Victoria J Davidson     | Signal Mountain   | 4.8    | 50      | Play Therapy, Anxiety         | (423) 464-4354     |
  | Blair Cobb             | Online Only      | 4.7    | 35      | Mindfulness, Stress           | (865) 813-8075     |

- **Dashboard:**
  - Review sentiment analysis heatmap.
