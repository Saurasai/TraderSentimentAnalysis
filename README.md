# 📈 Trader Performance vs Market Sentiment Analysis

![Streamlit](https://img.shields.io/badge/streamlit-app-blue)
![Python](https://img.shields.io/badge/python-3.13.5-green)
![Pandas](https://img.shields.io/badge/pandas-data%20analysis-blue)
![Matplotlib](https://img.shields.io/badge/matplotlib-visualization-orange)
![Seaborn](https://img.shields.io/badge/seaborn-stats%20visualization-blueviolet)

---

## Overview

This interactive Streamlit web application explores the relationship between **trader performance** and **market sentiment** (Fear & Greed Index) using historical trading and sentiment data.

The app provides a comprehensive analysis featuring:

* Summary statistics by sentiment category
* Statistical significance tests (T-tests)
* Time-series visualizations of trader profit and loss (PnL)
* Leverage analysis with graceful handling of missing data
* Trading volume comparisons
* Cumulative PnL tracking
* Sentiment lag impact on trading outcomes
* Symbol-wise performance insights
* Correlation heatmaps between key trading metrics

All insights are presented with **beautiful, dynamic visualizations** and **smooth animations** for an engaging user experience.

---

## Features

* **Interactive visualizations** powered by Matplotlib & Seaborn
* **Live Lottie animations** embedded to enhance UI/UX
* Robust handling of missing or incomplete data (e.g., leverage info)
* Modular, efficient, and well-documented codebase
* Fully self-contained — easy to run locally or deploy on the cloud

---

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/trader-sentiment-analysis.git
   cd trader-sentiment-analysis
   ```

2. Create a Python virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/Mac
   .\venv\Scripts\activate    # Windows
   ```

3. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. Make sure your data files are placed inside the `./data` folder:

   * `fear_greed_index.csv` (Market sentiment data)
   * `historical_data.csv` (Trader transaction data)

2. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

3. Open the URL provided in your terminal (usually `http://localhost:8501`) to interact with the app.

---



## Dependencies

* Python 3.13.5
* pandas
* matplotlib
* seaborn
* scipy
* streamlit
* streamlit-lottie
* requests

---

## Project Structure

```
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── data/                  # Input datasets (CSV files)
├── docs/
│   └── screenshots/       # Sample screenshots for README
└── README.md              # This documentation file
```


