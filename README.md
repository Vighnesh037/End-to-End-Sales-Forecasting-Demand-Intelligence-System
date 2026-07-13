# Retail Sales Forecasting & Inventory Intelligence

An end-to-end data science project that analyses historical retail sales, forecasts future demand, detects unusual sales patterns, segments products by demand behaviour, and presents the results through an interactive Streamlit dashboard.

## Project Overview

This project uses the Global Superstore dataset to support sales forecasting and inventory planning. The analysis covers historical sales trends, regional and category performance, time-series forecasting, anomaly detection, and product demand segmentation.

## Key Features

- Exploratory analysis of sales trends, categories and regions
- Monthly sales forecasting using SARIMA, Prophet and XGBoost
- Model comparison using MAE, RMSE and MAPE
- 3-month future sales forecast with confidence intervals
- Category and regional forecasting
- Detection of unusual sales periods
- Product demand segmentation for inventory planning
- Interactive Streamlit dashboard
- Executive business report with actionable recommendations


## Forecasting Models

Three forecasting approaches were developed and evaluated:

- SARIMA
- Facebook Prophet
- XGBoost

The models were evaluated on unseen historical data before being retrained on the complete dataset to generate the final three-month future forecast.

## Demand Segmentation

Products were grouped into four demand segments:

- High Volume, Core Demand
- High Value, High Volatility
- Low Volume, Stable Demand
- Emerging / Fast-Growing Demand

Each segment is linked to a different inventory and stocking strategy.

## Dashboard

The Streamlit dashboard provides interactive access to:

- Executive sales overview
- Forecast exploration
- Model performance comparison
- Anomaly detection results
- Product demand segments and stocking recommendations

## Installation

Clone the repository and install the required packages:

    pip install -r requirements.txt

Run the Streamlit application:

    streamlit run app.py

## Technologies Used

Python, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, Statsmodels, Prophet, XGBoost, Plotly and Streamlit.
Done as part of Xylofy AI internship 

## Author

Vighnesh C  
B.Tech Information Technology  
Government Engineering College Sreekrishnapuram
