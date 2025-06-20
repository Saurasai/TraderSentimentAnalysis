import streamlit as st
st.set_page_config(page_title="📈 Sentiment Analysis", layout="wide")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
from streamlit_lottie import st_lottie
import requests
import requests
import os
import streamlit as st

def download_csv_from_dropbox(dropbox_url, local_path):
    """
    Downloads a CSV file from a Dropbox shared link and saves it locally.
    Converts Dropbox shared URL to a direct download URL.
    """
    # Convert Dropbox share URL to direct download URL
    if "www.dropbox.com" in dropbox_url:
        direct_url = dropbox_url.replace("www.dropbox.com", "dl.dropboxusercontent.com").replace("?dl=0", "")
    else:
        direct_url = dropbox_url

    if not os.path.exists(local_path):
        r = requests.get(direct_url)
        if r.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(r.content)
            st.success(f"Downloaded file saved to {local_path}")
        else:
            st.error(f"Failed to download file: HTTP {r.status_code}")
    else:
        st.info(f"File {local_path} already exists, skipping download.")

# Dropbox link for your historical_data.csv
historical_data_url = "https://www.dropbox.com/scl/fi/d23gdpc2jidev7ipbt1wb/historical_data.csv?rlkey=j1vguqlbp8tx3sjvjev14frdk&st=neeo7dwj&dl=0"

# Call the function to download if not exists
download_csv_from_dropbox(historical_data_url, "./data/historical_data.csv")


# --- Load Lottie Animation with error handling ---
@st.cache_data
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Failed to load animation from {url}: {e}")
        return None

# Lottie animation URLs
analyze_anim_url = "https://assets7.lottiefiles.com/packages/lf20_jcikwtux.json"  # Example URL
chart_anim_url = "https://assets7.lottiefiles.com/packages/lf20_tll0j4bb.json"   # Example URL

analyze_anim = load_lottie_url(analyze_anim_url)
chart_anim = load_lottie_url(chart_anim_url)

# --- Header ---
col1, col2 = st.columns([2, 1])
with col1:
    st.title("📉 Trader Performance vs Market Sentiment")
    st.markdown("Analyze how traders perform under varying **fear & greed** conditions using visual and statistical analysis.")
with col2:
    if analyze_anim:
        st_lottie(analyze_anim, height=120, key="analyze")
    else:
        st.warning("Animation could not be loaded.")

# --- Load and process data ---
@st.cache_data
def load_data():
    sentiment_df = pd.read_csv('./data/fear_greed_index.csv')
    trader_df = pd.read_csv('./data/historical_data.csv')
    return sentiment_df, trader_df

sentiment_df, trader_df = load_data()

# Preprocessing
sentiment_df['date'] = pd.to_datetime(sentiment_df['date'])
trader_df['date'] = pd.to_datetime(trader_df['Timestamp IST'], format='%d-%m-%Y %H:%M').dt.floor('D')
trader_df['Side'] = trader_df['Side'].str.lower()
sentiment_df['classification'] = sentiment_df['classification'].astype('category')

# Aggregation
daily = trader_df.groupby('date').agg({
    'Closed PnL': 'sum',
    'Size USD': 'sum',
    'Account': 'nunique'
}).reset_index()

merged = pd.merge(daily, sentiment_df, on='date', how='inner')
merged = merged.sort_values('date')

# --- KPIs ---
st.subheader("📊 Key Metrics Summary")
col1, col2, col3 = st.columns(3)
col1.metric("📈 Total PnL", f"${merged['Closed PnL'].sum():,.2f}")
col2.metric("💰 Avg Daily Volume", f"${merged['Size USD'].mean():,.2f}")
col3.metric("👤 Total Traders", f"{merged['Account'].sum()}")

# --- Summary Table ---
st.markdown("### 🔎 Summary by Market Sentiment")
st.markdown(
    """
    This table summarizes the average, total, and count of Closed PnL values
    grouped by market sentiment classifications — Fear and Greed.
    """
)
summary = merged.groupby('classification')['Closed PnL'].agg(['mean', 'sum', 'count']).reset_index()
st.dataframe(summary, use_container_width=True)

# --- T-Test ---
st.markdown("### 📐 Statistical Significance Test")
st.markdown(
    """
    The independent t-test compares trader performance (Closed PnL) between Fear and Greed days.
    A low p-value (< 0.05) indicates a statistically significant difference in performance.
    """
)
fear = merged[merged['classification'] == 'Fear']['Closed PnL']
greed = merged[merged['classification'] == 'Greed']['Closed PnL']
t_stat, p_val = ttest_ind(fear, greed, equal_var=False)
st.info(f"**T-statistic**: `{t_stat:.4f}` &nbsp;&nbsp;&nbsp; **P-value**: `{p_val:.4f}`")

# --- Time Series ---
st.markdown("### 📆 PnL Over Time by Sentiment")
st.markdown(
    """
    This line chart shows the daily total Closed PnL over time, split by market sentiment classification.
    It helps visualize trends and differences in trader performance during Fear vs Greed periods.
    """
)
fig, ax = plt.subplots(figsize=(12, 4))
sns.lineplot(data=merged, x='date', y='Closed PnL', hue='classification', ax=ax)
st.pyplot(fig)

# --- Volume Analysis ---
st.markdown("### 💹 Trading Volume by Sentiment")
st.markdown(
    """
    This bar plot compares the average daily trading volume (Size USD) across different market sentiment states.
    It provides insight into whether traders trade more aggressively during Fear or Greed.
    """
)
fig, ax = plt.subplots()
sns.barplot(data=merged, x='classification', y='Size USD', ax=ax)
st.pyplot(fig)

# --- Cumulative PnL ---
st.markdown("### 📈 Cumulative Profit")
st.markdown(
    """
    This plot shows the cumulative profit (Closed PnL) over the entire period,
    highlighting how profits accumulate during Fear vs Greed market conditions.
    """
)
merged['Cumulative PnL'] = merged['Closed PnL'].cumsum()
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=merged, x='date', y='Cumulative PnL', ax=ax)
st.pyplot(fig)

# --- Lag Analysis ---
st.markdown("### 🔁 Impact of Previous Day Sentiment")
st.markdown(
    """
    This boxplot shows how the previous day's market sentiment potentially affects the current day's trader performance.
    It helps explore any lagging effect of sentiment on profitability.
    """
)
merged['prev_day_sentiment'] = merged['classification'].shift(1)
fig, ax = plt.subplots()
sns.boxplot(data=merged, x='prev_day_sentiment', y='Closed PnL', ax=ax)
st.pyplot(fig)

# --- Correlation Heatmap ---
st.markdown("### 🧠 Correlation Between Metrics")
st.markdown(
    """
    This heatmap displays correlations between key metrics like Closed PnL, trading volume (Size USD), and number of unique traders.
    Strong correlations can reveal interdependencies useful for strategy development.
    """
)
fig, ax = plt.subplots()
sns.heatmap(merged[['Closed PnL', 'Size USD', 'Account']].corr(), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# --- Footer with animation ---
st.markdown("---")
col1, col2 = st.columns([1, 2])
with col1:
    if chart_anim:
        st_lottie(chart_anim, height=100)
    else:
        st.warning("Footer animation could not be loaded.")
with col2:
    st.markdown("**Made By Sourabh Kumar Singh | Powered by Streamlit & Python**")
