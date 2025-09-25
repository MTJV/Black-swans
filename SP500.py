

import sys
import streamlit as st
print("Running with:", sys.executable)
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from st_autorefresh = st.autorefresh
st_autorefresh(interval=1 * 60 * 60 * 1000) #refreshes data every hour 

try:
    import streamlit as st
    USE_STREAMLIT = True
except ImportError:
    USE_STREAMLIT = False


ticker = '^GSPC'  # S&P 500 index symbol
data = yf.download(ticker, start='2000-01-01', progress=False, auto_adjust=False)

print(data.head())
print("Columns:", data.columns.tolist)

#Compute daily returns
data['Return'] = data['Adj Close'].pct_change()  #See masterdoc for ADJ CLOSE details 
                                            
#Rolling 30 day volatility
data['Rolling_vol'] = data['Return'].rolling(window=30).std() # Masterdoc, rolling window = 30 means 30 days

#Streamlit title for both streamlit and non-streamlit modes
if USE_STREAMLIT:
    st.title("S&P 500 Dashboard")
else:
    print("S&P 500 Dashboard")


# --- Histogram of Returns ---
fig1, ax1 = plt.subplots(figsize=(10,6))
ax1.hist(data["Return"].dropna(), bins=100, edgecolor="blue") #here Return is the daily return column we created above
ax1.set_title("S&P 500 Daily Returns Histogram")
ax1.set_xlabel("Daily Return")
ax1.set_ylabel("Frequency")

if USE_STREAMLIT:
    st.pyplot(fig1)
else:
    plt.show()


# --- Rolling Volatility ---
fig2, ax2 = plt.subplots(figsize=(10,6))
ax2.plot(data.index, data["Rolling_vol"], color="blue") # Plotting the rolling volatility, data index is the date (x axis) and rolling vol is the y axis
ax2.set_title("S&P 500 30-Day Rolling Volatility")
ax2.set_xlabel("Date")
ax2.set_ylabel("Rolling Volatility (Std Dev of Daily Returns)")

if USE_STREAMLIT:
    st.pyplot(fig2)
else:
    plt.show()
plt.ylabel('Rolling Volatility (Std Dev of Daily returns)')
