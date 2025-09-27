# 📊 Nigerian Price Tracker – Data Engineering Pipeline

### 📌Project Overview

This project implements a scalable data engineering pipeline on AWS to track and analyze product prices in Nigeria.

**Data Ingestion →** AWS Lambda scrapes product prices from multiple government and public sources and stores raw data in Amazon S3 (Bronze Layer).

**Data Processing** → AWS Glue cleans, transforms, and structures the raw files into analysis-ready datasets in S3 (Silver Layer).

**Data Orchestration →** AWS Step Functions automate the workflow (ingestion → transformation → storage) with error handling and retries.

**Data Consumption →** Processed datasets (Gold Layer) are connected to Power BI for interactive dashboards and insights.

This setup follows the modern data lake architecture with Bronze, Silver, and Gold layers, enabling scalability, automation, and cost efficiency.

### 🌍 Project Impact

Transparency in Market Prices → Provides citizens, businesses, and policymakers with up-to-date product prices across Nigeria.

Data-Driven Decisions → Enables researchers and organizations to analyze price fluctuations, inflation, and regional disparities.

Accessibility → Cloud-native pipeline ensures data is queryable and visualizable at scale.

Scalability for Future Growth → Extendable to other sectors (agriculture, energy, trade) and supports predictive analytics for price forecasting.

### ⚙️ Architecture
![pipeline Architecture](./Doc/Architecture%20diagram.jpg)

### 🚀 Setup Instructions

1️⃣ Prerequisites

Terraform
 installed

AWS account with programmatic access (IAM user with AdministratorAccess recommended for testing)

Python 3.9+ for Lambda functions

2️⃣ Infrastructure Deployment

Clone this repository:

git clone https://github.com/zalihat/Nigerian-Price-Watch.git
cd nigerian-price-watch


Initialize Terraform:

terraform init


Apply the infrastructure:

terraform apply


This will create:

S3 buckets (Bronze, Silver, Gold layers)

Lambda ingestion function

AWS Glue jobs for cleaning/transformation

Step Functions workflow

3️⃣ Running the Pipeline

The Step Function orchestrates the pipeline.

It will:

Trigger the Lambda scraper to pull fresh data into Bronze (S3).

Run Glue transformations to produce Silver and Gold datasets.

Store final outputs in Gold (S3) for Power BI.

4️⃣ Visualization in Power BI

Open Power BI Desktop.

Connect to the S3 Gold bucket via AWS Athena
.

Build dashboards to analyze price trends.

📂 Repository Structure

          

💡 Future Enhancements

Add CI/CD pipeline for Terraform + Lambda deployment

Integrate Airflow on MWAA for complex orchestration

Build real-time dashboards with AWS QuickSight or Kafka + Spark streaming


🏆 Impact Statement

This project demonstrates how cloud-based data engineering can drive transparency, accessibility, and decision-making in emerging economies.
By enabling citizens, policymakers, and businesses to analyze prices at scale, it supports economic planning, inflation tracking, and market research in Nigeria.

